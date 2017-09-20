from latlon_util import find_dir


# North should print 90
pos1 = (-1.3945, 50.8926)
pos2 = (-1.3945, 51.8926)
print(find_dir(pos1, pos2))

# East should print 0
pos1 = (-1.3945, 50.8926)
pos2 = (1.3945, 50.8926)
print(find_dir(pos1, pos2))

# South should print 270
pos1 = (-1.3945, 50.8926)
pos2 = (-1.3945, 45.8926)
print(find_dir(pos1, pos2))

# WEST Should print 180
pos1 = (-1.3945, 50.8926)
pos2 = (-1.4005, 50.8926)
print(find_dir(pos1, pos2))
