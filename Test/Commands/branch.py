from M8085._branch import Branch
from M8085 import Register

branch = Branch()

branch_inst = branch.get_inst()

branch_inst['CALL']('2050H')

r = Register()

print(r['PC']) 
print(r['SP']) 