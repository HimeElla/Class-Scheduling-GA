import random, copy
from Classes import *
from math import ceil, log2
import math

Group.groups = [Group("13 SI 1", 31), Group("13 SI 2", 29), Group("12 SI 1", 25),
                Group("12 SI 2", 27), Group("11 SI 1", 20), Group("11 SI 2", 31)]

Dosen.dosen = [Dosen("Samuel"), Dosen("Tennov"), Dosen("Mona"),
                        Dosen("Mario"), Dosen("Albert"), Dosen("Zico")]

Matakuliah.matkul = [Matakuliah("SISOP", is_lab=True), Matakuliah("CERTAN"), Matakuliah("ALSRUDAT", is_lab=True),
                       Matakuliah("BASDAT"), Matakuliah("BASDATLAN"),
                       Matakuliah("Prog2", is_lab=True), Matakuliah("MPSI"), Matakuliah("JARKOM")]

Ruangan.ruang = [Ruangan("516", 60), Ruangan("722", 100), Ruangan("714", 100, is_lab=True),
              Ruangan("725", 40, is_lab=True), Ruangan("934", 70)]

Jadwal.sesi = [Jadwal("08:00", "09:50", "Senin"), Jadwal("10:00", "11:50", "Senin"), Jadwal("13:00", "14:50", "Senin"), Jadwal("15:00", "16:50", "Senin"),
              Jadwal("08:00", "09:50", "Selasa"), Jadwal("10:00", "11:50", "Selasa"), Jadwal("13:00", "14:50", "Selasa"), Jadwal("15:00", "16:50", "Selasa"),
              Jadwal("08:00", "09:50", "Rabu"), Jadwal("10:00", "11:50", "Rabu"), Jadwal("13:00", "14:50", "Rabu"), Jadwal("15:00", "16:50", "Rabu"),
              Jadwal("08:00", "09:50", "Kamis"), Jadwal("10:00", "11:50", "Kamis"), Jadwal("13:00", "14:50", "Kamis"), Jadwal("15:00", "16:50", "Kamis"),
              Jadwal("08:00", "09:50", "Jumat"), Jadwal("10:00", "11:50", "Jumat"), Jadwal("13:00", "14:50", "Jumat"), Jadwal("15:00", "16:50", "Jumat")]

# Group.groups = []
# Dosen.dosen = []
# Matakuliah.Classes = []
# Ruangan.ruang =[]                                   

# TODO
# 0.  Running Simplified Class Scheduling - Done
# 0.5 Problem Instance to Binary String - Done
# 1.  Multiple days - Done
# 2.  Class Size - Done
# 2.25 Check Selection Function - Done
# 2.5 One group can attend only one class at a time - Done
# 3.  Multiple matkul - Done
# 4.  Lab - Done

# Below chromosome parts are just to teach basic

# cpg = ["000000", "010001", "100100", "111010"] # course, professor, student group pair
# lts = ["00", "01"] # lecture theatres
# sesi = ["00", "01"] # time sesi

# ######### Chromosome ##############
# <Matakuliah, Prof, Group, Jadwal, LT>   #
# ###################################

max_score = None

cpg = []
lts = []
sesi = []
bits_needed_backup_store = {}  # to improve performance

def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)

def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res

def convert_input_to_bin():
    global cpg, lts, sesi, max_score

    cpg = [Matakuliah.find("SISOP"), Dosen.find("Tennov"), Group.find("14 SI 1"),
           Matakuliah.find("SISOP lab"), Dosen.find("Zico"), Group.find("14 SI 2"),
           Matakuliah.find("CERTAN"), Dosen.find("Samuel"), Group.find("13 SI 1"),
           Matakuliah.find("ALSRUDAT"), Dosen.find("Tennov"), Group.find("13 SI 2"),
           Matakuliah.find("ALSRUDAT lab"), Dosen.find("Albert"), Group.find("12 SI 1"),
           Matakuliah.find("BASDAT"), Dosen.find("Mona"), Group.find("12 SI 2"),
           Matakuliah.find("MPSI"), Dosen.find("Mona"), Group.find("13 SI 1"),
           Matakuliah.find("BASDATLAN"), Dosen.find("Mario"), Group.find("11 SI 1"),
           Matakuliah.find("Prog2"), Dosen.find("Mario"), Group.find("11 SI 2")
           ]

    for _c in range(len(cpg)):
        if _c % 3:  # Matakuliah
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Matakuliah.matkul), '0')
        elif _c % 3 == 1:  # Dosen
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Dosen.dosen), '0')
        else:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Group.groups), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Ruangan.ruang)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Ruangan.ruang), '0'))

    for t in range(len(Jadwal.sesi)):
        sesi.append((bin(t)[2:]).rjust(bits_needed(Jadwal.sesi), '0'))

    # print(cpg)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3

def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(Matakuliah.matkul)]

def professor_bits(chromosome):
    i = bits_needed(Matakuliah.matkul)

    return chromosome[i: i + bits_needed(Dosen.dosen)]

def group_bits(chromosome):
    i = bits_needed(Matakuliah.matkul) + bits_needed(Dosen.dosen)

    return chromosome[i:i + bits_needed(Group.groups)]

def slot_bits(chromosome):
    i = bits_needed(Matakuliah.matkul) + bits_needed(Dosen.dosen) + \
        bits_needed(Group.groups)

    return chromosome[i:i + bits_needed(Jadwal.sesi)]

def lt_bits(chromosome):
    i = bits_needed(Matakuliah.matkul) + bits_needed(Dosen.dosen) + \
        bits_needed(Group.groups) + bits_needed(Jadwal.sesi)

    return chromosome[i: i + bits_needed(Ruangan.ruang)]

def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0

# Memeriksa agar jadwal matakuliah yang diajarkan satu dosen tidak bentrok.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and professor_bits(chromosome[i]) == professor_bits(chromosome[j]):
                clash = True
                # print("These prof. have clashes")
                # print_chromosome(chromosome[i])
                # print_chromosome(chromosome[j])
        if not clash:
            scores = scores + 1
    return scores

# Memeriksa agar jadwal matakuliah dari satu group tidak bentrok.
def group_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and\
                    group_bits(chromosomes[i]) == group_bits(chromosomes[j]):
                # print("These matkul have slot/lts clash")
                # print_chromosome(chromosomes[i])
                # print_chromosome(chromosomes[j])
                # print("____________")
                clash = True
                break
        if not clash:
            # print("These matkul have no slot/lts clash")
            # print_chromosome(chromosomes[i])
            # print_chromosome(chromosomes[j])
            # print("____________")
            scores = scores + 1
    return scores

# Memeriksa matakuliah berada di kelas yang kosong.
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                # print("These matkul have slot/lts clash")
                # printChromosome(chromosome[i])
                # printChromosome(chromosome[j])
                clash = True
        if not clash:
            scores = scores + 1
    return scores

# Memeriksa apakah ukuran kelas cukup untuk satu group.
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Group.groups[int(group_bits(_c), 2)].size <= Ruangan.ruang[int(lt_bits(_c), 2)].size:
            scores = scores + 1
    return scores

# Memeriksa apakah jenis kelas tepat dengan jenis matakuliah (lab/teori).
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Matakuliah.matkul[int(course_bits(_c), 2)].is_lab == Ruangan.ruang[int(lt_bits(_c), 2)].is_lab:
            scores = scores + 1
    return scores

# Memeriksa apakah suatu kelas berada pada jadwal yang tepat (tidak bentrok dengan teori).
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Matakuliah.matkul[int(course_bits(_c), 2)].is_lab == Jadwal.sesi[int(slot_bits(_c), 2)].is_lab_slot:
            scores = scores + 1
    return scores

# Menghitung jumlah score chromosomes yang sudah tepat.
def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + group_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    return score / max_score

def cost(solution):
    # solution would be an array inside an array
    # it is because we use it as it is in genetic algorithms
    # too. Because, GA require multiple solutions i.e population
    # to work.
    return 1 / float(evaluate(solution))

def init_population(n):
    global cpg, lts, sesi
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(sesi) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes

# Memodifikasi kombinasi dari Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    rand_slot = random.choice(sesi)
    rand_lt = random.choice(lts)

    a = random.randint(0, len(chromosome) - 1)
    
    chromosome[a] = course_bits(chromosome[a]) + professor_bits(chromosome[a]) +\
        group_bits(chromosome[a]) + rand_slot + rand_lt

    # print("After mutation: ", end="")
    # printChromosome(chromosome)

def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    
def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()

# Mencetak chromosome ke layar
def print_chromosome(chromosome):
    print(Jadwal.sesi[int(slot_bits(chromosome), 2)], "\t|\t",
          Matakuliah.matkul[int(course_bits(chromosome), 2)], " (",
          Dosen.dosen[int(professor_bits(chromosome), 2)], ")\t|\t",
          Group.groups[int(group_bits(chromosome), 2)], "\t|\t",
          Ruangan.ruang[int(lt_bits(chromosome), 2)])

# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab
def ssn(solution):
    rand_slot = random.choice(sesi)
    rand_lt = random.choice(lts)
    
    a = random.randint(0, len(solution) - 1)
    
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + rand_slot + lt_bits(solution[a])
    return [new_solution]

# Swapping Neighborhoods
# It randomy selects two matkul and swap their time sesi
def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + slot_bits(solution[b]) + lt_bits(solution[a])

    new_solution[b] = course_bits(solution[b]) + professor_bits(solution[b]) +\
        group_bits(solution[b]) + temp + lt_bits(solution[b])
    return [new_solution]

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    alpha = 0.9
    T = 1.0
    T_min = 0.00001
    
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])

    for __n in range(500):
        new_solution = swn(population[0])
        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            population = new_solution
            old_cost = new_cost
        T = T * alpha
    # print(population)
    # print("Cost of altered solution: ", cost(population[0]))
    print("\nScore: ", evaluate(population[0]))
    print("\n----------------------- Schedule -----------------------\n")
    for lec in population[0]:
        print_chromosome(lec)

def genetic_algorithm():
    generation = 0
    convert_input_to_bin()
    population = init_population(3)

    # print("Original population: ", population)
    print("\n----------------------- Genetic Algorithm -----------------------\n")
    while True:
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            print("Generations:", generation)
            print("Best Chromosome fitness value", evaluate(max(population, key=evaluate)))
            print("Best Chromosome: ", max(population, key=evaluate))
            for lec in max(population, key=evaluate):
                print_chromosome(lec)
            break
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                
                # selection(population[_c], len(cpg))
                mutate(population[_c])

        generation = generation + 1
        # print("Gen: ", generation)
    # print("Population", len(population))


def main():
    # n = int(input("Masukkan jumlah Group: "))
    # for i in range (0, n):
    #     element = [input("Nama: "), int(input("Size: "))]
    #     groups(element)

    # n = int(input("Masukkan jumlah Dosen: "))
    # for i in range (0, n):
    #     element = input("Nama: ")
    #     dosen.append(element)

    # n = int(input("Masukkan jumlah Matakuliah: "))
    # for i in range (0, n):
    #     element = input("Code: ")
    #     Matakuliah.append(element)

    # n = int(input("Masukkan jumlah Ruangan: "))
    # for i in range (0, n):
    #     element = [input("Nama: "), int(input("Size: "))]
    #     Ruangan.append(element)

    random.seed()
    genetic_algorithm()
    simulated_annealing()

main()
