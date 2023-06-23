from jhu_assembly_linter.linter import Finding


def test_finding_column_range():
    finding = Finding(
        message='Error found.',
        line_number=14,
        columns=(4, 9),
        source='The error is here...',
    )
    assert str(finding) == '\n'.join((
        'Error found.',
        '14: The error is here...',
        '        ^^^^^',
    ))


def test_finding_column_zero():
    finding = Finding(
        message='Error found.',
        line_number=14,
        columns=(0,),
        source='The error is here...',
    )
    assert str(finding) == '\n'.join((
        'Error found.',
        '14: The error is here...',
        '    ^',
    ))


def test_finding_column_no_columns():
    finding = Finding(
        message='Error found.',
        line_number=14,
        source='The error is here...',
    )
    assert str(finding) == '\n'.join((
        'Error found.',
        '14: The error is here...',
    ))


def test_finding_column_no_line_number():
    finding = Finding(
        message='Error found.',
        columns=(0,),
        source='The error is here...',
    )
    # Don't show source if line_number is 0.
    assert str(finding) == '\n'.join((
        'Error found.',
    ))


def test_finding_column_no_source():
    finding = Finding(
        message='Error found.',
        line_number=1,
        columns=(0,),
    )
    # Only show message if no source.
    assert str(finding) == '\n'.join((
        'Error found.',
    ))
