class LinearRegression():
    
    def __init__(self, x_points, y_points):
        if not x_points:
            raise ValueError("x_points is empty")
        
        if not y_points:
            raise ValueError("y_points is empty")
    
        if len(x_points) != len(y_points):
            raise ValueError("x_points and y_points must have the same length")
    
        self.x_points = x_points
        self.y_points = y_points
        self.coef = None
        self.intercept = None
        
    def fit(self):
        a = self._covarianza(self.x_points, self.y_points, self._media(self.x_points), self._media(self.y_points)) / self._varianza(self.x_points, self._media(self.x_points))
        b = self._media(self.y_points) - a * self._media(self.x_points)
        
        self.coef = a
        self.intercept = b
    
    def _media(self, x):
        return sum(x) / len(x)
    
    def _covarianza(self, x, y, mean_x, mean_y):
        sumatory = 0
        
        for i in range(len(x)):
            
            sumatory += (x[i] - mean_x) * (y[i] - mean_y)
            
        return sumatory / len(x)
    
    def _varianza(self, x, mean_x):
        sumatory = 0
        
        for i in range(len(x)):
            
            sumatory += (x[i] - mean_x) ** 2
            
        result = sumatory / len(x)
            
        return result if result != 0 else 1