class Hash:
    """This hash deals with colisions simply by appending the colision in a list. This way, we will need to rehash everytime we
    get a list with too much keys, to avoid a linear search in the hash."""
    def __init__(self):
        self.Codification = 171 #Number in which we will codify all information
        self.Keys = [[] for i in range(self.Codification)]  #Each key will be in a array of arrays.
        self.Objects = [[] for i in range(self.Codification)] #Each object corresponds to a key
        self.MaxLenBucket = 13
        #self.NumberRehash = 0 !!!Debug only!!!


    def GetFirstKeyValue(self, Key):
        KeyValue = 0
        if isinstance(Key, str):
            for i in range(0, len(Key)):
                KeyValue += (ord(Key[i]) - 65) *(i+1)

        KeyValue = KeyValue % self.Codification
        return KeyValue

    def Append(self, Key, Object):
        KeyValue = self.GetFirstKeyValue(Key)

        if Key in self.Keys[KeyValue]:
            self.Remove(Key)

        self.Keys[KeyValue].append(Key)
        self.Objects[KeyValue].append(Object)

        if self.CheckRehash(KeyValue):
            self.Rehash()
        return

    def Check(self, Key):
        KeyValue = self.GetFirstKeyValue(Key)

        if Key in self.Keys[KeyValue]:  #self.Keys[KeyValue] returns a list with every key in the position of the hash
            Position = self.Keys[KeyValue].index(Key)
            return self.Objects[KeyValue][Position]

        else:
            return False

    def Remove(self, Key):
        KeyValue = self.GetFirstKeyValue(Key)

        if Key in self.Keys[KeyValue]:
            Position = self.Keys[KeyValue].index(Key)
            self.Keys[KeyValue].pop(Position)
            self.Objects[KeyValue].pop(Position)
        return

    def CheckRehash(self, KeyValue):
        """The only case we will make a rehash in this hash is if any of the buckets is len > MaxLenBucket."""
        if len(self.Keys[KeyValue]) > self.MaxLenBucket:
            return True
        else:
            return False

    def Rehash(self):
        ListKeys = []
        ListObjects = []

        for Bucket in self.Keys:
            for Key in Bucket:
                ListKeys.append(Key)
                ListObjects.append(self.Check(Key))

        for Key in ListKeys:
            self.Remove(Key)

        self.Codification = (self.Codification * 2) + 1
        self.Keys = [[] for i in range(self.Codification)]
        self.Objects = [[] for i in range(self.Codification)]

        for i in range(0, len(ListKeys)-1):
            self.Append(ListKeys[i],ListObjects[i])
        return

if __name__ == "__main__":  #Debug only
    Reshi = Hash()
    Reshi.Append('a', 'a')
    Reshi.Append('b', 'b')
    Reshi.Append('c', 'd')
    Reshi.Append('c', 'c')
    Reshi.Append('e', 'e')
    Reshi.Append('g', 'g')
    Reshi.Append('i', 'i')
    Reshi.Append('k', 'k')
    Reshi.Append('l', 'l')

    print(Reshi.Keys)
    print(Reshi.Objects)
