import re


class Finding:
    def __init__(
        self,
        line_nubmer: int,
        message: str,
        columns: tuple,
    ) -> None:
        self.line_nubmer = line_nubmer
        self.message = message
        self.columns = columns


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

        # Program Name: helloWorld.s
        # Author: John Doe
        # Date: 11/11/2020
        # Purpose: To print out a hello world message using a
        #          system call (svc) from ARM assembly
        # Functions: (when applicable)
        # Inputs: (when applicable)
        # Outputs: (when applicable)

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

        # Good Examples
        helloWorld.s
        toBeOrNotToBe.s
        multiplyNumbers.s
        addNumbers.s
        # Bad Example 1 - Starts with uppercase
        HelloWorld.s
        # Bad Example 2 - Starts with numerical value
        2beOrNot2Be.s
        # Bad Example 3 - Snake case and all caps
        MULTIPLY_NUMBERS.s
        # Bad Example 4 - hyphenated and all lowercase
        add-numbers.s
        """

    def _check_file_name_main(self):
        """
        Check that if file has "main" function, it has "Main" in its name.

        # Good Example
        calculateHeightMain.s
        # Bad Example 3 - not clear where main lives
        calculateHeight.s
        """
        for i, line in enumerate(self._lines, start=1):
            if self._check_is_comment_line(line):
                continue

            if self._check_is_instruction_line(line):
                continue

            if line.strip().startswith('main:') and not self.file.endswith('Main.s'):
                self._findings.append(Finding(
                    i,
                    'File name does not contain "Main" when it should.',
                    (0,),
                ))
                break

    def _check_data_section_follows_text_section(self):
        """
        Check that all data sections follow text sections.
        """

    def _check_instructions_uppercase(self):
        """
        Check that instructions are uppercase.

        .text
        .global main
        main:
            # Prompts user for an input
            LDR r0, =userPrompt
            BL printf
        """
        for i, line in enumerate(self._lines, start=1):
            if not self._check_is_instruction_line(line):
                continue

            if not line.strip().split()[0].isupper():
                self._findings.append(Finding(
                    i,
                    'Instruction is not uppercase.',
                    (len(line) - len(line.lstrip()),),
                ))

    def _check_registers_lowercase(self):
        """
        Check registers are listed in lowercase.

        .text
        .global main
        main:
            # Prompts user for an input
            LDR r0, =userPrompt
            BL printf
        """
        for i, line in enumerate(self._lines, start=1):
            if not self._check_is_instruction_line(line):
                continue

            chunk = line
            m = True  # To get things started.
            pos = 0
            while m:
                m = re.match(r'[ ,]R\d{1,16}[ ,]', chunk)
                if m:
                    self._findings.append(Finding(
                        i,
                        'Register is not lowercase.',
                        (pos + m.start(),),
                    ))
                    pos += m.start()
                    chunk = line[pos:]

    def _check_line_empty_with_nonzero_space(self):
        """
        Check check that empty lines have no trailing whitespace.

        .text
        .global main
        main:
            # Prompts user for an input
            LDR r0, =userPrompt
            BL printf
        """
        for i, line in enumerate(self._lines, start=1):
            if len(line) > 0 and len(line.strip()) == 0:
                self._findings.append(Finding(
                    i,
                    'Non-functional whitespace found.',
                    (0, len(line)),
                ))

    def _check_spaces(self):
        """
        Check each non-comment line to check that it does not have tabs.
        """
        for i, line in enumerate(self._lines, start=1):
            try:
                self._findings.append(Finding(
                    i,
                    'Tab found. Only spaces allowed.',
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
