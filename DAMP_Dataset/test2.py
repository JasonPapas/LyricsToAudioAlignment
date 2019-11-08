import os.path as p

StatInfo_AllStar = p.getsize(r"SongLyrics/all star.txt")
print(StatInfo_AllStar)
StatInfo_Animal = p.getsize(r"SongLyrics/animal.txt")
print(StatInfo_Animal)
# class A():
#     def __init__(self, listA=[]):
#         self.listA = listA
#         self.listB = []
    
#     def change(self, temp):
#         self.listA += temp
#         self.listB += temp
    
# a=A()
# b=A()

# a.listA = [1,2]
# b.listA = [3,4]
# b.listA.append(70)
# a.listA.append(50)

# a.listB = [5,6]
# b.listB = [7,8]

# print(f"a.problem = {a.listA}")
# print(f"a.listB = {a.listB}")
# print(f"b.problem = {b.listA}")
# print(f"b.listB = {b.listB}")

# a.change("hello")
# print(f"a.listA = {a.listA}")
# print(f"a.listB = {a.listB}")