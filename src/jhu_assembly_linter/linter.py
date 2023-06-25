import os
import re
import string

from .finding import Finding


class Linter:
    # Oh, type checking...
    SENTIAL_EMPTY_LINES = []

    def __init__(self, file: str) -> None:
        self._file_path = file
        self._file: str = os.path.basename(self._file_path)
        self._findings: list[Finding] = []
        self.__lines: list[str] = self.SENTIAL_EMPTY_LINES

    @property
    def _lines(self):
        if self.__lines is self.SENTIAL_EMPTY_LINES:
            with open(self._file_path) as fp:
                self.__lines = fp.readlines()
        return self.__lines

    def lint(self):
        self._check_preamble()
        self._check_file_name()
        self._check_file_name_main()
        self._check_data_section_follows_text_section()
        self._check_instructions_uppercase()
        self._check_registers_lowercase()
        self._check_line_empty_with_nonzero_space()
        self._check_spaces()

    def _check_preamble(self):
        """
        Ensure the preamble is present and well formatted.
        """
        preamble = []
        for i, line in enumerate(self._lines, start=1):
            if not self._check_is_comment_line(line):
                break

            preamble.append((i, line.strip().lstrip('#').lstrip()))

        line_by_key: dict[str, tuple] = {}
        for i, line in preamble:
            key = line.split()
            if not key:
                continue

            key = key[0].rstrip(':').strip().lower()
            line_by_key[key] = (i, line)

        program_line = line_by_key.get('program') or ()
        if not program_line:
            self._findings.append(Finding(
                'Preamble error: No "Program Name" line found.',
            ))
        else:
            self._check_preamble_program_line(*program_line)

        author_line = line_by_key.get('author')
        if not author_line:
            self._findings.append(Finding(
                'Preamble error: No "Author" line found.',
            ))
        else:
            self._check_preamble_author_line(*author_line)

        date_line = line_by_key.get('date')
        if not date_line:
            self._findings.append(Finding(
                'Preamble error: No "Date" line found.',
            ))
        else:
            self._check_preamble_date_line(*date_line)

        purpose_line = line_by_key.get('purpose')
        if not purpose_line:
            self._findings.append(Finding(
                'Preamble error: No "Purpose" line found.',
            ))
        else:
            self._check_preamble_purpose_line(*purpose_line)

        functions_line = line_by_key.get('functions')
        if not functions_line:
            self._findings.append(Finding(
                'Preamble error: No "Functions" line found.',
            ))
        else:
            self._check_preamble_functions_line(*functions_line)

    def _check_file_name(self):
        """
        Check the file name follows the correct conventions.
        """
        name = self._file[:-2]

        invalidChars = set(name) - set(string.ascii_letters)
        if invalidChars:
            self._findings.append(Finding(
                f'File name contains invalid characters: {invalidChars}',
            ))

        if name[0] not in string.ascii_lowercase:
            self._findings.append(Finding(
                'File starts with non-lowercase letter.',
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
                if not self._file.endswith('Main.s'):
                    self._findings.append(Finding(
                        'File name does not end with "Main" when it should.',
                        line_number=i,
                        source=line,
                    ))
                break
        else:
            if self._file.endswith('Main.s'):
                self._findings.append(Finding(
                    'File name ends with "Main" but no main function found.',
                ))

    def _check_data_section_follows_text_section(self):
        """
        Check that all data sections follow text sections.
        """
        # TODO: Make this loop reset on new functions.
        can_see_data = False
        for i, line in enumerate(self._lines, start=1):
            if line.strip().startswith('.text'):
                can_see_data = True
                continue

            if line.strip().startswith('.data'):
                if can_see_data:
                    can_see_data = False
                    continue
                else:
                    self._findings.append(Finding(
                        'Data sections must follow a text section.',
                        line_number=i,
                        source=line,
                    ))

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
                    line_number=i,
                    columns=(len(line) - len(line.lstrip()),),
                    source=line,
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
                        line_number=i,
                        columns=(pos + m.start(),),
                        source=line,
                    ))
                    pos += m.end() - 1
                    chunk = line[pos:]

    def _check_line_empty_with_nonzero_space(self):
        """
        Check check that empty lines have no trailing whitespace.
        """
        for i, line in enumerate(self._lines, start=1):
            tmp_line = line.replace('\r', '').replace('\n', '')
            if len(tmp_line) > 0 and len(line.strip()) == 0:
                self._findings.append(Finding(
                    'Non-functional whitespace found.',
                    line_number=i,
                    columns=(0, len(line)),
                    source=line,
                ))

    def _check_spaces(self):
        """
        Check each non-comment line to check that it does not have tabs.
        """
        for i, line in enumerate(self._lines, start=1):
            try:
                self._findings.append(Finding(
                    'Tab found. Only spaces allowed.',
                    line_number=i,
                    columns=(line.index('\t'),),
                    source=line,
                ))
            except ValueError:
                pass

    def _check_is_comment_line(self, line: str):
        return bool(re.match(r'^\s*#', line))

    def _check_is_function_line(self, line: str):
        return bool(re.match(r'^[_a-zA-Z0-9]+:\s*$', line))

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

    def _check_preamble_program_line(self, line_number, line):
        parts = list(map(str.strip, line.split(':')))
        if len(parts) != 2:
            self._findings.append(Finding(
                'Invalid "Program Name" line found.',
                line_number=line_number,
                source=line,
            ))

        if parts[0] != 'Program Name':
            self._findings.append(Finding(
                'Invalid "Program Name" line found.',
                line_number=line_number,
                source=line,
                columns=(0, len(parts[0])),
            ))

        if parts[1] != self._file:
            self._findings.append(Finding(
                'File in "Program Name" is not equivalent to file name.',
                line_number=line_number,
                source=line,
                columns=(line.index(':') + 2, len(line)),
            ))

    def _check_preamble_author_line(self, line_number, line):
        # TODO: Implement a more sophisticated check.
        pass

    def _check_preamble_date_line(self, line_number, line):
        # TODO: Implement a more sophisticated check.
        pass

    def _check_preamble_purpose_line(self, line_number, line):
        # TODO: Implement a more sophisticated check.
        pass

    def _check_preamble_functions_line(self, line_number, line):
        # Get functions from function line.
        line_functions = set(line.split()[1:])

        # Get functions from file.
        file_functions = set()
        for tmp_line in self._lines:
            if self._check_is_function_line(tmp_line):
                file_functions.add(tmp_line.strip().rstrip(':'))

        # function in line but not in file
        missing_functions = line_functions - file_functions
        if missing_functions:
            for missing_function in missing_functions:
                i = line.index(missing_function)
                self._findings.append(Finding(
                    f'Function {missing_function} listed in '
                    'Functions line but not in file.',
                    line_number=line_number,
                    source=line,
                    columns=(i, i + len(missing_function)),
                ))

        # function in line but not in file
        missing_functions = file_functions - line_functions
        if missing_functions:
            for missing_function in missing_functions:
                self._findings.append(Finding(
                    f'Function {missing_function} in file '
                    'but not listed in Functions line.',
                    line_number=line_number,
                    source=line,
                ))

    @property
    def findings(self) -> list[Finding]:
        return self._findings
