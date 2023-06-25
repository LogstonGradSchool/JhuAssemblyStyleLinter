
class Finding:
    def __init__(
        self,
        message: str,
        line_number: int = 0,
        columns: tuple = (),
        source: str = '',
    ) -> None:
        self.message = message
        self.line_number = line_number
        self.columns = columns
        self.source = source

        if not self.source:
            if self.line_number > 0:
                raise ValueError('Line number set but no source given.')
            elif len(self.columns) > 0:
                raise ValueError('Columns set but no source given.')

    def __str__(self) -> str:
        lines = [f'E:: {self.message}']
        if self.line_number:
            line_prefix = f'{self.line_number}: '
            line_prefix_len = len(line_prefix)
            lines.append(line_prefix + self.source.rstrip())
            carrot_line = ' ' * line_prefix_len
            if len(self.columns) == 2:
                carrot_line += ' ' * self.columns[0]
                carrot_line += '^' * (self.columns[1] - self.columns[0])
                lines.append(carrot_line)
            elif len(self.columns) == 1:
                carrot_line += ' ' * self.columns[0]
                carrot_line += '^'
                lines.append(carrot_line)

        return '\n'.join(lines)

    __repr__ = __str__
