class Symbol:
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent_scope = parent
        self.name = name
        self.symbols = {}
        self.v_type = {}
        self.v_dims = {}
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get(name)
        else:
            print("Symbol \"" + name + "\" not found, Scope: " + self.name, self.symbols)
    #
    def get_v_dims(self, name):
        if name in self.v_dims:
            return self.v_dims[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get_v_dims(name)
        else:
            print("Symbol \"" + name + "\" not found, Scope: " + self.name, self.symbols)


    def get_v_type(self, name):
        if name in self.v_type:
            return self.v_type[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get_v_type(name)
        else:
            print("Symbol \"" + name + "\" not found, Scope: " + self.name, self.symbols)

    #
    def getParentScope(self):
        return self.parent_scope
    #

    def pushScope(self, name):
        return SymbolTable(self, name)
    #

    def popScope(self):
        return self.parent_scope
    #
