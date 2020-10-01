import main



class Point :
	def __init__(self , x,y):
		self.x = x 
		self.y = y 



def rectCollision(rect1 , rect2):
	P11 = (rect1[0] ,rect1[1])
	P12 = (rect1[0] + rect1[2], rect1[1] )
	P13 = (rect1[0] , rect1[1] + rect1[3])
	P14 = (rect1[0] + rect1[2] ,rect1[1] + rect1[3] )
    
	def inBox(point , rect ):
    	if (point[0] <= rect[0] + rect[2] and point[0] >= rect[0] and point[1] <= rect[1] + rect[3] and point[1] >= rect[1] ):
    		pass
    # 	return True
    # else : 
    # 	return False



def main():
	
	rect1 = (0 , 0 , 20 , 30 )
	rect2 = (2 , 2 , 20 , 30 )

	if rectCollision(rect1, rect2) : 
		print('collision')

if __name__ =='__main__' :
	main()