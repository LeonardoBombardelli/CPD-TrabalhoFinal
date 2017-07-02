class Hash:
    """This hash dealswith colisions simply by appending the colision in a list. This way, we will need to rehash everytime we
    get a list with too much keys, to avoid a linear search in the hash."""
    def __init__(self):
        self.Codification = 137 #Number in which we will codify all information
        self.Keys = [[] for i in range(137)]  #Each key will be in a array of arrays.
        self.Objects = [[] for i in range(137)] #Each object corresponds to a key
        self.MaxLenBucket = 5


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
            for Key in self.Keys[Bucket]:
                ListKeys.append(Key)
                List.Keys.append(self.Check(Key))

        for Key in ListKeys:
            self.Remove(Key)

        self.Codification = (self.Codification * 2) + 1
        self.Keys = [[] for i in range(self.Codification)]
        self.Objects = [[] for i in range(self.Codification)]

        for i in range(0, len(ListKeys)-1):
            self.Append(ListKeys[i],ListObjects[i])
        return

Reshi = Hash()
Reshi.Append('a', 'a')
Reshi.Remove('a')
print(Reshi.Objects)
print(Reshi.Keys)
