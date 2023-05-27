import subprocess

class BazelBuildozerWrapper:
    def __init__(self, workspace_path, buildozer_path):
        self.workspace_path = workspace_path
        self.buildozer_path = buildozer_path

    def execute_command(self, command, target):
        full_command = [self.buildozer_path] + [command] + [target]
        print(' '.join(full_command))
        try:
            output = subprocess.run(full_command, cwd=self.workspace_path, capture_output=True, check=True)
            print(output.stdout)
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def run_buildozer_command(self, command, target):
        self.execute_command(command, target)

    def add_attribute_value(self, target, attribute, value):
        command = f"add {attribute} {value}"
        self.execute_command(command, target)

    def replace_attribute_value(self, target, attribute, old_value, new_value):
        command = f"replace {attribute} {old_value} {new_value}"
        self.execute_command(command, target)

    def add_load_statement(self, target, path, symbols):
        command = f"new_load {path} {symbols}"
        self.execute_command(command, target + ":__pkg__")

    def replace_load_statement(self, target, path, symbols):
        command = f"replace_load {path} {symbols}"
        self.execute_command(command, target + ":__pkg__")

    # def substitute_load(self, target, old_regexp, new_template):
    #     command = f"substitute_load {old_regexp} {new_template}"
    #     self.execute_command(command, target)

    # def comment(self, target, attribute=None, value=None, comment=""):
    #     if attribute and value:
    #         command = f"comment {attribute} {value} {comment}"
    #     elif attribute:
    #         command = f"comment {attribute} {comment}"
    #     else:
    #         command = f"comment {comment}"
    #     self.execute_command(command, target)

    # def print_comment(self, target, attribute=None, value=None):
    #     if attribute and value:
    #         command = f"print_comment {attribute} {value}"
    #     elif attribute:
    #         command = f"print_comment {attribute}"
    #     else:
    #         command = "print_comment"
    #     self.execute_command(command, target)

    def delete(self, target):
        command = "delete"
        self.execute_command(command, target)

    # def move(self, target, old_attr, new_attr, values):
    #     command = f"move {old_attr} {new_attr} {values}"
    #     self.execute_command(command, target)

    def new_rule(self, target, rule_kind, rule_name, relative_rule=None, position=""):
        if relative_rule:
            command = f"new {rule_kind} {rule_name} {position} {relative_rule}"
        else:
            command = f"new {rule_kind} {rule_name} {position}"
        self.execute_command(command, target)

    def print_attribute(self, target, attributes):
        command = f"print {' '.join(attributes)}"
        self.execute_command(command, target)

    def remove_attribute(self, target, attribute):
        command = f"remove {attribute}"
        self.execute_command(command, target)

    def remove_attribute_value(self, target, attribute, values):
        command = f"remove {attribute} {values}"
        self.execute_command(command, target)

    # def remove_comment(self, target, attribute=None, value=None):
    #     if attribute and value:
    #         command = f"remove_comment {attribute} {value}"
    #     elif attribute:
    #         command = f"remove_comment {attribute}"
    #     else:
    #         command = "remove_comment"
    #     self.execute_command(command, target)

    # def remove_if_equal(self, target, attribute, value):
    #     command = f"remove_if_equal {attribute} {value}"
    #     self.execute_command(command, target)

    def rename_attribute(self, target, old_attr, new_attr):
        command = f"rename {old_attr} {new_attr}"
        self.execute_command(command, target)

    def set_attribute(self, target, attribute, values):
        command = f"set {attribute} {values}"
        self.execute_command(command, target)

    def set_if_absent_attribute(self, target, attribute, values):
        command = f"set_if_absent {attribute} {values}"
        self.execute_command(command, target)

