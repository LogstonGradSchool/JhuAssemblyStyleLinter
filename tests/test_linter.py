from jhu_assembly_linter.linter import Linter


def test_check_preamble():
    assert False


def test_check_file_name():
    # Good names.
    linter = Linter("helloWorld.s")
    linter._check_file_name()
    assert len(linter.findings) == 0

    linter = Linter("toBeOrNotToBe.s")
    linter._check_file_name()
    assert len(linter.findings) == 0

    linter = Linter("multiplyNumbers.s")
    linter._check_file_name()
    assert len(linter.findings) == 0

    linter = Linter("addNumbers.s")
    linter._check_file_name()
    assert len(linter.findings) == 0

    # Bad names.
    linter = Linter("HelloWorld.s")
    linter._check_file_name()
    assert len(linter.findings) == 1

    linter = Linter("2beOrNot2Be.s")
    linter._check_file_name()
    assert len(linter.findings) == 2

    linter = Linter("MULTIPLY_NUMBERS.s")
    linter._check_file_name()
    assert len(linter.findings) == 2

    linter = Linter("add-numbers.s")
    linter._check_file_name()
    assert len(linter.findings) == 1


def test_check_file_name_main():
    linter = Linter("doesNotEndInCorrectWord.s")
    linter._Linter__lines = [
        '# A comment',
        '.text',
        'main:',
        'MOV r0, r0',
    ]
    linter._check_file_name_main()
    assert len(linter.findings) == 1
    assert linter.findings[0].line_nubmer == 3

    linter = Linter("doesEndInMain.s")
    linter._Linter__lines = [
        '# A comment',
        '.text',
        'main:',
        'MOV r0, r0',
    ]
    linter._check_file_name_main()
    assert len(linter.findings) == 0

    linter = Linter("doesNotContainMain.s")
    linter._Linter__lines = [
        '# A comment',
        '.text',
        'otherFunc:',
        'MOV r0, r0',
    ]
    linter._check_file_name_main()
    assert len(linter.findings) == 1
    assert linter.findings[0].line_nubmer == 4

    linter = Linter("doesNotMatter.s")
    linter._Linter__lines = [
        '# A comment',
        '.text',
        'otherFunc:',
        'MOV r0, r0',
    ]
    linter._check_file_name_main()
    assert len(linter.findings) == 0


def test_check_data_section_follows_text_section():
    assert False


def test_check_instructions_uppercase():
    linter = Linter("")
    linter._Linter__lines = [
        'MOV r0, r0',
        'Mov r0, r0',
        'mov r0, r0',
    ]
    linter._check_instructions_uppercase()
    assert len(linter.findings) == 2
    assert linter.findings[0].line_nubmer == 2
    assert linter.findings[1].line_nubmer == 3


def test_check_registers_lowercase():
    linter = Linter("")
    linter._Linter__lines = [
        'MOV r0, r0',
        'MOV R0, r0',
        'MOV R0, R0',
    ]
    linter._check_registers_lowercase()
    assert len(linter.findings) == 3
    assert linter.findings[0].line_nubmer == 2
    assert linter.findings[1].line_nubmer == 3
    assert linter.findings[2].line_nubmer == 3


def test_check_line_empty_with_nonzero_space():
    linter = Linter("")
    linter._Linter__lines = [
        '    ',
        '\t',
        '    MOV r0, r0',
    ]
    linter._check_line_empty_with_nonzero_space()
    assert len(linter.findings) == 2
    assert linter.findings[0].line_nubmer == 1
    assert linter.findings[1].line_nubmer == 2


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
    linter = Linter("")
    assert linter._check_is_instruction_line('MOV r0, r0')
    assert not linter._check_is_instruction_line('# MOV r0, r0')
    assert not linter._check_is_instruction_line('.global')
    assert not linter._check_is_instruction_line('.text')
    assert not linter._check_is_instruction_line('main:')
    assert not linter._check_is_instruction_line('')
