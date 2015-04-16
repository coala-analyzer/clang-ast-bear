from coalib.bears.LocalBear import LocalBear
import clang.cindex as ci


class ClangASTBear(LocalBear):
    def analyze_function(self,
                           cursor,
                           filename,
                           stack=None):
        if stack is None:
            stack = []
        file = cursor.location.file
        name = None if file is None else file.name.decode()

        if str(name) == str(filename):
            self.debug("Got child:")
            self.debug("STACK:", *stack, delimiter="\n")
            self.debug("KIND:", str(cursor.kind))
            self.debug("FILE:", str(name))
            self.debug("USR :", str(cursor.get_usr()))
            self.debug("DISP:", str(cursor.displayname))
            if cursor.is_definition():
                self.debug("DEFI:", str(cursor.get_definition()))

        stack.append(str(cursor.kind))
        for child in cursor.get_children():
            self.print_clang_cursor(child, filename, stack=stack)
        stack.pop()

    def print_clang_cursor(self,
                           cursor,
                           filename,
                           indent="",
                           stack=None,
                           max_recursion=20):
        if stack is None:
            stack = []

        if len(indent) > max_recursion*2:
            print("ABORTING")
            return

        if cursor.kind == ci.CursorKind.DECL_REF_EXPR:
            self.analyze_function(cursor,
                                  filename)
        else:
            for child in cursor.get_children():
                self.print_clang_cursor(child, filename, stack=stack)

    def run(self, filename, file, *args):
        index = ci.Index.create()
        tree = index.parse(filename)

        self.print_clang_cursor(tree.cursor, filename)
