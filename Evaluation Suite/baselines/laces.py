n,m=map(int,input().split())
friends_list = [[] for _ in range(n)]
for i in range(m):
	a,b = map(int, input().split())
	friends_list[a-1].append(b)
	friends_list[b-1].append(a)
# so idea: we keep track of the number of the number of laces each student is tied to.
# that way, if we remove a student, we can update the list in constant time
def reprimand(friends_list):
	bad_list = []
	for index in range(n):
		neighbours = friends_list[index]
		if len(neighbours) == 1:
			bad_list.append(index)
	for index in bad_list:
		neighbours = friends_list[index]
		friends_list[index] = []
		try:
			friends_list[neighbours[0]-1].remove(index+1)
		except IndexError: # already deleted
			pass

ans = 0
copy = [len(stuff) for stuff in friends_list]
another = []
while copy != another:
	another = copy
	reprimand(friends_list)
	copy = [len(stuff) for stuff in friends_list]
	ans += 1
print(ans-1)