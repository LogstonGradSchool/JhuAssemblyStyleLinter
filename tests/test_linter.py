from jhu_assembly_linter.linter import Linter


def test_check_preamble():
    assert False


def test_check_file_name():
    assert False


def test_check_file_name_main():
    assert False


def test_check_data_section_follows_text_section():
    assert False

def test_check_instructions_uppercase():
    assert False


def test_check_registers_lowercase():
    assert False


def test_check_line_empty_with_nonzero_space():
    assert False


def test_check_spaces():
    linter = Linter("")
    linter._Linter__lines = [
        '# A comment line',
        '# Something with \t tabs',
        '\tMOV r0, r0',
    ]
    linter._check_spaces()
    assert len(linter.findings) == 2
    assert linter.findings[0].line_nubmer == 2
    assert linter.findings[1].line_nubmer == 3


def test_check_is_comment_line():
    linter = Linter("")
    assert linter._check_is_comment_line('# this is a comment line')
    assert linter._check_is_comment_line('   # this is a poorly indented comment line')
    assert not linter._check_is_comment_line('MOV r0, r0')
    assert not linter._check_is_comment_line('.global func')
    assert not linter._check_is_comment_line('main:')


def test_check_is_instruction_line():
    assert False
