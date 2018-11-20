# Классы и наследование

import sys
import os.path
import csv

class CarBase:

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
    
    @property
    def car_type(self):
        pass

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def photo_file_name(self):
        return self._photo_file_name

    @photo_file_name.setter
    def photo_file_name(self, value):
        self._photo_file_name = value

    def get_photo_file_ext(self):
        try:
            ext = os.path.splitext(self.photo_file_name)[1]
        except:
            ext = ''
        return ext

    @property
    def carrying(self):
        return self._carrying

    @carrying.setter
    def carrying(self, value):
        self._carrying = value


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count
        
    @property
    def car_type(self):
        return "car"

    @property
    def passenger_seats_count(self):
        return self._passenger_seats_count

    @passenger_seats_count.setter
    def passenger_seats_count(self, value):
        self._passenger_seats_count = value

class Truck(CarBase):

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl

    @property
    def car_type(self):
        return "truck"

    @property
    def body_length(self):
        return self._body_length
    
    @property
    def body_width(self):
        return self._body_width

    @property
    def body_height(self):
        return self._body_height

    @property
    def body_whl(self):
        return self._body_whl

    @body_whl.setter
    def body_whl(self, value):
        self._body_whl = value

        if len(value) == 0:
            _body_length, _body_width, _body_height = 0.0, 0.0, 0.0
        else:
            try:
                _body = value.split("x")
                self._body_length = float(_body[0]) 
                self._body_width  = float(_body[1])
                self._body_height = float(_body[2])
            except ValueError:
                self._body_length, self._body_width, self._body_height = 0.0, 0.0, 0.0 

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height 


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @property
    def car_type(self):
        return "spec_machine"

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, value):
        self._extra = value


def get_car_list(csv_filename):
    car_list = []

    if csv_filename is not None:
        try:
            with open(csv_filename, "r", newline="") as csv_fd:
                reader = csv.reader(csv_fd, delimiter=';')
                next(reader)  # пропускаем заголовок
                for row in reader:
                    try:

                        if (len(row) == 7): 
                            
                            brand           = row[1]
                            photo_file_name = row[3]
                            carrying        = float(row[5])

                            if (row[0] == 'car'):                          
                                passenger_seats_count = int(row[2])
                                car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))


                            if (row[0] == 'truck'):
                                bodywhl = row[4]
                                car_list.append(Truck(brand, photo_file_name, carrying, bodywhl))

                            if (row[0] == 'spec_machine'):
                                extra = row[6]
                                car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))

                    except ValueError:
                        print("Error convert value")
                    except:
                       print("Error read row")

        except IOError as e:
            print("Cannot open file: {0}. I/O error({1}): {2}".format(csv_filename, e.errno, e.strerror))  
        except: #handle other exceptions such as attribute errors
            print("Cannot open file: {0}. Unexpected error: {1}".format(csv_filename, sys.exc_info()[0])) 
    else:
        print("File name: None. Set file name.")

    return car_list

if __name__ == '__main__':
    FILENAME = r"C:\Users\User\py\geoip\coursera_week3_cars.csv"
    print(get_car_list(FILENAME))