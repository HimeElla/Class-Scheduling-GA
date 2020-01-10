class Group:
    groups = None

    def __init__(self, name, size):
        self.name = name
        self.size = size

    # Mencari nama suatu grup di dalam class Group
    @staticmethod
    def find(name):
        for i in range(len(Group.groups)):
            if Group.groups[i].name == name:
                return i
        return -1

    def __repr__(self):
        return self.name


class Dosen:
    dosen = None

    def __init__(self, name):
        self.name = name

    # Mencari nama dosen dari class Dosen
    @staticmethod
    def find(name):
        for i in range(len(Dosen.dosen)):
            if Dosen.dosen[i].name == name:
                return i
        return -1

    def __repr__(self):
        return self.name


class Matakuliah:
    matkul = None

    def __init__(self, name, is_lab=False):
        self.name = name
        self.is_lab = is_lab

    # Mencari matakuliah berdasarkan kode matakuliah
    @staticmethod
    def find(name):
        for i in range(len(Matakuliah.matkul)):
            if Matakuliah.matkul[i].name == name:
                return i
        return -1

    def __repr__(self):
        return self.name


class Ruangan:
    ruangan = None

    def __init__(self, name, size, is_lab=False):
        self.name = name
        self.size = size
        self.is_lab = is_lab

    # Mencari ruangan berdasarkan nama ruangan
    @staticmethod
    def find(name):
        for i in range(len(Ruangan.ruang)):
            if Ruangan.ruang[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Gd. " + self.name


class Jadwal:
    sesi = None

    def __init__(self, start, end, day, is_lab_slot=False):
        self.start = start
        self.end = end
        self.day = day
        self.is_lab_slot = is_lab_slot

    # Mengembalikan waktu jadwal per sesi dengan format "Hari jam mulai - jam berakhir"
    def __repr__(self):
        return self.day + "\t" + self.start + "-" + self.end
