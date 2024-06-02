import pytest

from tasks import ProgramException, StudyDatabase, check_copilot


def test_copilot_fix_formatting():
    assert check_copilot("""
  MOV       R0  1111
MOV R1 2


       ADD R3   R8                      
         
         MOV R3 0
""")[0] == """MOV R0 1111
MOV R1 2
ADD R3 R8
MOV R3 0
"""


def test_copilot_fix_instruction_name():
    assert check_copilot("""
  MXV       R0  1111
MOW R1 2
VDD R3   R8                      
ADV R3 0
""")[0] == """MOV R0 1111
MOV R1 2
ADD R3 R8
ADD R3 0
"""


def test_copilot_skip_duplicated_lines():
    assert check_copilot("""
  MOV       R0  1111
MOV R0 1111
MXV R0   1111   

ADD R3 R8
ADD R4 R8
ADD R3 R8
ADX R3 R8
ADD R3 R8
MOV R3 0
""")[0] == """MOV R0 1111
ADD R3 R8
ADD R4 R8
ADD R3 R8
MOV R3 0
"""


def test_copilot_execute_simple():
    assert check_copilot("""
MOV R0 5
MOV R1 8
ADD R0 R1
""")[1] == 13


def test_copilot_execute_indexing():
    assert check_copilot("""
MOV R0 5
MOV R1 8
MOV [R0] R1
ADD [R0] 8
ADD [5] 2
MOV R1 5
MOV R0 [R1]
""")[1] == 18


def test_copilot_execute_duplicated():
    assert check_copilot("""
MOV R0 5
ADD R0 1
AXD R0 1
ADZ R0 1
ADD R0 1
""")[1] == 6


def test_copilot_invalid_set_constant():
    with pytest.raises(ProgramException):
        check_copilot("MOV 0 5")


def test_copilot_invalid_instruction():
    with pytest.raises(ProgramException):
        check_copilot("AI R0 5")
    with pytest.raises(ProgramException):
        check_copilot("A R0 5")
    with pytest.raises(ProgramException):
        check_copilot("IAMAI R0 5")


def test_copilot_invalid_indexing():
    with pytest.raises(ProgramException):
        check_copilot("MOV [R0 5")
    with pytest.raises(ProgramException):
        check_copilot("MOV [[R0]] 5")


def test_copilot_invalid_arguments():
    with pytest.raises(ProgramException):
        check_copilot("MOV 5")
    with pytest.raises(ProgramException):
        check_copilot("MOV")
    with pytest.raises(ProgramException):
        check_copilot("MOV R0 R1 R2")


def test_db_empty():
    db = StudyDatabase()
    assert db.passed_subjects() == []
    assert db.average_points_per_type("lesson") == {}
    assert db.average_points_per_type("test") == {}
    assert db.average_points_per_type("project") == {}
    assert db.total_points_per_subject() == {}
    assert db.total_points_per_subject("lesson") == {}
    assert db.total_points_per_subject("test") == {}
    assert db.total_points_per_subject("project") == {}


def test_db_single_subject():
    db = StudyDatabase()
    assert db.add_points("UTI", "lesson", 5) == 5
    assert db.add_points("UTI", "lesson", 10) == 15

    assert db.passed_subjects() == []
    assert db.average_points_per_type("lesson") == {"UTI": 7}
    assert db.average_points_per_type("test") == {"UTI": 0}
    assert db.average_points_per_type("project") == {"UTI": 0}
    assert db.total_points_per_subject() == {"UTI": 15}

    assert db.add_points("UTI", "test", 40) == 40
    assert db.passed_subjects() == ["UTI"]
    assert db.average_points_per_type("lesson") == {"UTI": 7}
    assert db.average_points_per_type("test") == {"UTI": 40}
    assert db.total_points_per_subject() == {"UTI": 55}
    assert db.total_points_per_subject("lesson") == {"UTI": 15}
    assert db.total_points_per_subject("test") == {"UTI": 40}
    assert db.total_points_per_subject("project") == {"UTI": 0}


def test_db_passed():
    db = StudyDatabase()
    assert db.add_points("UTI", "lesson", 5) == 5
    assert db.add_points("UTI", "lesson", 10) == 15
    assert db.add_points("SKJ", "lesson", 5) == 5
    assert db.add_points("SKJ", "lesson", 5) == 10
    assert db.add_points("SKJ", "lesson", 4) == 14
    assert db.add_points("UTI", "test", 35) == 35
    assert db.add_points("SKJ", "test", 55) == 55

    assert db.passed_subjects() == ["SKJ"]
    assert db.add_points("UTI", "lesson", 5)
    assert db.passed_subjects() == ["SKJ", "UTI"]


def test_db_total_points():
    db = StudyDatabase()
    assert db.add_points("UTI", "lesson", 5) == 5
    assert db.add_points("UTI", "lesson", 10) == 15
    assert db.add_points("SKJ", "lesson", 5) == 5
    assert db.add_points("SKJ", "lesson", 5) == 10
    assert db.add_points("SKJ", "lesson", 4) == 14
    assert db.add_points("UTI", "test", 35) == 35
    assert db.add_points("SKJ", "test", 55) == 55

    assert db.total_points_per_subject() == {"SKJ": 69, "UTI": 50}
    assert db.total_points_per_subject("lesson") == {"SKJ": 14, "UTI": 15}
    assert db.total_points_per_subject("test") == {"SKJ": 55, "UTI": 35}
    assert db.total_points_per_subject("project") == {"SKJ": 0, "UTI": 0}


def test_db_average_points():
    db = StudyDatabase()
    assert db.add_points("UTI", "lesson", 5) == 5
    assert db.add_points("UTI", "lesson", 10) == 15
    assert db.add_points("SKJ", "lesson", 5) == 5
    assert db.add_points("SKJ", "lesson", 5) == 10
    assert db.add_points("SKJ", "lesson", 4) == 14
    assert db.add_points("UTI", "test", 35) == 35
    assert db.add_points("SKJ", "test", 55) == 55

    assert db.average_points_per_type("lesson") == {"SKJ": 4, "UTI": 7}
    assert db.average_points_per_type("test") == {"UTI": 35, "SKJ": 55}
    assert db.average_points_per_type("project") == {"UTI": 0, "SKJ": 0}
