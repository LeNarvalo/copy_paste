from math import sqrt

def Methodic(a,n): #TopAndRight
	r = 0
	c = 0
	k = -1
	lT = []
	lR= []
	
	while len(lT)<int(n/4):
		for x in a[r][c:k]:
			lT.append(x)
		
		for row in a[r:k]:
			lR.append(row[k])

		r+=1
		c+=1
		k-=1

	return BottomAndLeft(a,n,lT,lR)

def BottomAndLeft(a,n,lT,lR):
	r = 0
	c = 0
	k = -1
	i = 0
	lB = []
	lL = []
	
	while len(lB)<int(n/4):
		for x in a[::-1][r][::-1][c:k]:
			lB.append(x)
		
		for row in a[::-1][r:k]:
			lL.append(row[i])
	
		r+=1
		c+=1
		k-=1
		i+=1

	return lT,lR,lB,lL

def Spiral(m, n, a, x, r=1): 
  
	# Large array to initialize it 
	# with elements of matrix 
	b = [0]*x 
  
	#/* k - starting row index 
	#l - starting column index*/ 
	k, l = 0, 0
  
	# Counter for single dimension array 
	# in which elements will be stored 
	z = 0
  
	# Total elements in matrix 
	size = m * n 
  
	while (k < m and l < n): 
		  
		# Variable to store value of matrix. 
		val = 0
  
		# Print the first row  
		# from the remaining rows  
		for i in range(l, n):			  
			val = a[k][i] 
			b[z] = val 
			z += 1

		k += 1
  
		# Print the last column 
		# from the remaining columns 
		for i in range(k, m): 
			val = a[i][n-1] 
			b[z] = val 
			z += 1
  
		n -= 1
  
		# Print the last row  
		# from the remaining rows 
		if (k < m): 
			for i in range(n - 1, l - 1, -1): 
				val = a[m - 1][i] 
				b[z] = val 
				z += 1
  
		m -= 1
  
		# Print the first column  
		# from the remaining columns  
		if (l < n): 
			for i in range(m - 1, k - 1, -1): 
				val = a[i][l] 
				b[z] = val 
				z += 1
			l += 1

	return b[::r]
	#for i in range(size - 1, -1, -1): 
	 #   print(b[i], end = " ") 
		
  
# Driver Code
#a=[]
#b=[]
#x=100#nombre de crops
#for c in range(x):
#	b.append(c)
#	if len(b) == sqrt(x):
#		a.append(b)
#		b = []
##ReversespiralPrint(len(a), len(a[0]), a, x)
#e, f, g, h = Methodic(a,x)
        
