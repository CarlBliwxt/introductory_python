
from statistics import mean, median
from time import sleep
import trafficComponents as tc
import destinations as d 


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):

        self.time = 0
        self.lane = tc.Lane(11)
        self.lane_west = tc.Lane(8)
        self.lane_south = tc.Lane(8)
        self.light_west = tc.Light(14,6)
        self.light_south = tc.Light(14,4)
        self.destination = d.Destinations()
        self.exit_west = 0
        self.exit_south = 0
        self.vehicle_counter = 0
        self.que = []
        self.blocked = 0
        self.que_count = 0
        self.exitedCars = []
        self.west_time = []
        self.south_time = []

    def snapshot(self):
        print(f'{self.light_west}, {self.lane_west}, {self.lane}, {self.que},') 
        print(f'{self.light_south}, {self.lane_south}')
        

    def step(self):
        
        self.time += 1

        if tc.Light.is_green(self.light_west):
            if self.lane_west.get_first() != None: 
                self.exit_west += 1
                current = self.lane_west.get_first()
                exit_time = current.born_time()
                time = abs(self.time - exit_time)
                self.west_time.append(time)
            self.lane_west.remove_first()
                
        
               
        if self.light_south.is_green():
            if self.lane_south.get_first() != None:
                self.exit_south += 1  
                current = self.lane_south.get_first()
                exit_time = current.born_time()
                time = abs(self.time - exit_time)
                self.south_time.append(time)
            self.lane_south.remove_first()
                
        tc.Lane.step(self.lane_west)
        tc.Lane.step(self.lane_south)
        
        char = str(tc.Lane.get_first(self.lane))
        print(char)

        if char == "W" : 
            if tc.Lane.is_last_free(self.lane_west) == True:
                bil = tc.Lane.remove_first(self.lane)
                self.lane_west.enter(bil)
            else: 
                self.blocked += 1
        if char == "S" : 
            if tc.Lane.is_last_free(self.lane_south) == True:
                bil = tc.Lane.remove_first(self.lane)
                self.lane_south.enter(bil)
            else: 
                self.blocked += 1
                print( self.blocked)

    
        tc.Lane.step(self.lane)

        temp_des = self.destination.step()
        if temp_des != None:
            vehicle = tc.Vehicle(temp_des, self.time)
            self.vehicle_counter += 1
        if tc.Lane.is_last_free(self.lane): 
            if len(self.que) > 0:
                self.que_count += 1
                self.lane.enter(self.que.pop(0))
                if  temp_des != None:
                    self.que.append(vehicle)
                    self.que_count += 1
            else:
                if temp_des != None:
                    self.lane.enter(vehicle)
        else: 
            if temp_des != None:
                self.que.append(vehicle)
                self.que_count += 1
        

        
        tc.Light.step(self.light_south)
        tc.Light.step(self.light_west)


    def in_system(self):
       in_lane = self.lane.number_in_lane()
       lane_west = self.lane_west.number_in_lane()
       lane_south = self.lane_south.number_in_lane()
       que = len(self.que) 
       sumof = in_lane + lane_west + lane_south + que 
       return sumof 
    

    def print_statistics(self):
        self.west_time = sorted(self.west_time)
        self.south_time = sorted(self.south_time)
        west_time_average = round(sum(self.west_time)/len(self.west_time),2)
        south_time_average = round(sum(self.south_time)/len(self.south_time),2)
        print(' this is blocked', self.blocked)
        print(f'Statistics after {self.time} timesteps:      \n')
        print(f'Created vehicles:{self.vehicle_counter}')
        print(f'Cars in system:  {self.in_system()}\n')
        print(f'At exit          West:          South:')
        print(f'Vehicles out:    {self.exit_west}             {self.exit_south}')
        print(f'Minimal time:    {self.west_time[0]}             {self.south_time[0]}')
        print(f'Maximal time:    {self.west_time[-1]}             {self.south_time[-1]}')
        print(f'Mean time:       {west_time_average}          {south_time_average}')
        print(f'Median time:     {self.west_time[len(self.west_time)//2]}             {self.south_time[len(self.south_time)//2]} \n')
        print(f'Blocked:         {(self.blocked/self.time)*100} %       ')
        print(f'Queue            {(self.que_count/self.time)*100} %             ')
        


def main():
    ts = TrafficSystem()
    for i in range(100):
        ts.snapshot()
        ts.step()
        sleep(0)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    main()
