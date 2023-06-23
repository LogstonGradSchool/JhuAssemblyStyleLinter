import re
import string


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


class Linter:
    # Oh, type checking...
    SENTIAL_EMPTY_LINES = []

    def __init__(self, file: str) -> None:
        self.file: str = file
        self._findings: list[Finding] = []
        self.__lines: list[str] = self.SENTIAL_EMPTY_LINES

    @property
    def _lines(self):
        if self.__lines is self.SENTIAL_EMPTY_LINES:
            with open(self.file) as fp:
                self.__lines = fp.readlines()
        return self.__lines

    def lint(self):
        self._check_preamble()
        self._check_spaces()

    def _check_preamble(self):
        """
        Ensure the preamble is present and well formatted.
        """
        preamble = []
        for line in self._lines:
            if not self._check_is_comment_line(line):
                break
            preamble.append(line)

        if len(preamble) < 3:
            pass

    def _check_file_name(self):
        """
        Check the file name follows the correct conventions.
        """
        name = self.file[:-2]

        invalidChars = set(name) - set(string.ascii_letters)
        if invalidChars:
            self._findings.append(Finding(
                f'File name contains invalid characters: {invalidChars}',
            ))

        if name[0] not in string.ascii_lowercase:
            self._findings.append(Finding(
                f'File starts with non-lowercase letter.',
            ))

    def _check_file_name_main(self):
        """
        Check that if file has "main" function, it has "Main" in its name.
        """
        for i, line in enumerate(self._lines, start=1):
            if self._check_is_comment_line(line):
                continue

            if self._check_is_instruction_line(line):
                continue

            if line.strip().startswith('main:'):
                if not self.file.endswith('Main.s'):
                    self._findings.append(Finding(
                        'File name does not contain "Main" when it should.',
                        i,
                        (0,),
                    ))
                break
        else:
            if self.file.endswith('Main.s'):
                self._findings.append(Finding(
                    'File name contains "Main" but no main function found.',
                ))


    def _check_data_section_follows_text_section(self):
        """
        Check that all data sections follow text sections.
        """

    def _check_instructions_uppercase(self):
        """
        Check that instructions are uppercase.
        """
        for i, line in enumerate(self._lines, start=1):
            if not self._check_is_instruction_line(line):
                continue

            if not line.strip().split()[0].isupper():
                self._findings.append(Finding(
                    'Instruction is not uppercase.',
                    i,
                    (len(line) - len(line.lstrip()),),
                ))

    def _check_registers_lowercase(self):
        """
        Check registers are listed in lowercase.
        """
        for i, line in enumerate(self._lines, start=1):
            if not self._check_is_instruction_line(line):
                continue

            chunk = line
            m = True  # To get things started.
            pos = 0
            while m:
                m = re.search(r'[ ,]R\d{1,16}([ ,])?', chunk)
                if m:
                    self._findings.append(Finding(
                        'Register is not lowercase.',
                        i,
                        (pos + m.start(),),
                    ))
                    pos += m.end() - 1
                    chunk = line[pos:]

    def _check_line_empty_with_nonzero_space(self):
        """
        Check check that empty lines have no trailing whitespace.
        """
        for i, line in enumerate(self._lines, start=1):
            if len(line) > 0 and len(line.strip()) == 0:
                self._findings.append(Finding(
                    'Non-functional whitespace found.',
                    i,
                    (0, len(line)),
                ))

    def _check_spaces(self):
        """
        Check each non-comment line to check that it does not have tabs.
        """
        for i, line in enumerate(self._lines, start=1):
            try:
                self._findings.append(Finding(
                    'Tab found. Only spaces allowed.',
                    i,
                    (line.index('\t'),),
                ))
            except ValueError:
                pass

    def _check_is_comment_line(self, line: str):
        return bool(re.match(r'^\s*#', line))

    def _check_is_instruction_line(self, line: str) -> bool:
        """
        Return true if line holds operation instructions.
        """
        # Ignore comment lines.
        if self._check_is_comment_line(line):
            return False

        # Ignore empty lines.
        if not line.strip():
            return False

        # Ignore empty lines that start sections.
        if line.strip().startswith('.'):
            return False

        # Ignore function title lines.
        if ':' in line:
            return False

        return True

    @property
    def findings(self) -> list[Finding]:
        return self._findings
