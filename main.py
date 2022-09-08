"""

Satisfaction score parts:
Maximize (
  First cum first serve * ( 
    Away from screen - J -> 1 , A -> 0.1 
    Togetherness - Completly together -> 1 , 1 / number of splits
  ) * 0.5 + 0.5 * (Number of seats filled by actual people / ( Number of seats wasted + Number of actual people)) 
)

"""

from collections import defaultdict
import sys
import os

class Seat:
  def __init__(self, row, seatNumber):
    self.row = row
    self.seatNumber = seatNumber

class Group:
  def __init__(self, code, numberOfReservations, totalGroups, assignedSeats = []):
    self.code = code
    self.numberOfReservations = numberOfReservations
    self.assignedSeats = assignedSeats
    self.totalGroups = totalGroups

  def getCurrentSatisfaction(self):
    order = int(self.code[1:])
    orderSatisfaction = 1 - ( order - 1 ) / self.totalGroups
    seatSatisfaction = 0
    for seat in self.assignedSeats:
      seatSatisfaction += (( ord(seat.row) - ord('A') + 1) / 10)
    seatSatisfaction /= len(self.assignedSeats)
    numberOfGroups = 1
    sortedSeatList = list(sorted(self.assignedSeats, key = lambda val: [val.row, val.seatNumber], reverse = True))
    for i in range(1, len(sortedSeatList)):
      if sortedSeatList[i].row != sortedSeatList[i-1].row or sortedSeatList[i].seatNumber != sortedSeatList[i-1].seatNumber-1:
        numberOfGroups += 1
    groupSatisfaction = 1 / numberOfGroups
    totalReservationSatisfaction = orderSatisfaction * ( seatSatisfaction + groupSatisfaction) / 2
    return totalReservationSatisfaction

  def getSeatArrangementString(self):
    sortedSeatList = list(sorted(self.assignedSeats, key = lambda val: [val.row, val.seatNumber], reverse = True))
    return ",".join(list(map(lambda item: item.row + str(item.seatNumber + 1), sortedSeatList)))
        


# def getSeatCompletion(availableSeats):
#   numberOfPeopleSeated = 0
#   numberOfSeatsWasted = 0
#   for i in availableSeats:
#     for j in i:
#       if j == 1:
#         numberOfPeopleSeated += 1
#       elif j == -1:
#         numberOfSeatsWasted += 1
#   return numberOfPeopleSeated / ( numberOfSeatsWasted + numberOfPeopleSeated)        

def occupySeats(availableSeats, seatsToBeOccupied):
  seatsPerRow = defaultdict(list)
  for seat in seatsToBeOccupied:
    seatsPerRow[seat[0]].append(seat)
  for row, seatsInRow in seatsPerRow.items():
    sortedSeatsInRow = sorted(seatsInRow, key = lambda item: [item[0], item[1]])
    startIndex = max(0, sortedSeatsInRow[0][1] - 3)
    endIndex = min(20 - 1, sortedSeatsInRow[-1][1] + 3)
    for i in range(startIndex, endIndex+1):
      availableSeats[row][i] = -1
    for i in sortedSeatsInRow:
      availableSeats[row][i[1]] = 1

def convertIndexToSeatObj(ind):
  return Seat(chr(ind[0] + ord('A')), ind[1])

def printAvailablty(availableSeats):
  for i in range(10):
    for j in range(20):
      if availableSeats[i][j] == 0:
        print('A', end='')
      elif availableSeats[i][j] == 1:
        print('O', end='')
      else:
        print('-', end='')
    print()
        

def main(path):
  data = []
  groups = []
  with open(path, "r") as f:
    for line in f.read().split("\n"):
      code, numberOfReservations = line.split(" ")
      data.append([code, int(numberOfReservations)])

  # As i need the total number of reservations(total groups) i will have to scan the data again.
  for code, numberOfReservations in data:
    groups.append(Group(code, numberOfReservations, len(data)))

  availableSeats = [[0 for j in range(20)] for i in range(10)]

  for group in groups:
    requiredSeats = group.numberOfReservations
    disjointArrangement = []
    nonDisjointArrangement = []
    prevAvailableSeat = None
    contigiousAvailableLength = 0
    for i in range(9,-1,-1):
      for j in range(19,-1,-1):
        if availableSeats[i][j] == 0:
          if len(disjointArrangement) < requiredSeats:
            disjointArrangement.append((i, j))
            #Nondisjointarrangement
          if prevAvailableSeat and prevAvailableSeat[0] == i and prevAvailableSeat[1] - 1 == j:
            contigiousAvailableLength += 1
            if contigiousAvailableLength == requiredSeats:
              for k in range(requiredSeats):
                nonDisjointArrangement.append((i,j+k))
          else:
            contigiousAvailableLength = 1
          prevAvailableSeat = [i, j]
        if len(disjointArrangement) == requiredSeats and len(nonDisjointArrangement) == requiredSeats:
          break
    #finding the Satisifaction which one tochoose
    # Cannot satisfy reservation
    if not disjointArrangement or len(disjointArrangement) != requiredSeats:
      continue

    
    disjointSatisfaction = Group(
      group.code, 
      group.numberOfReservations, 
      len(groups), 
      list(map(convertIndexToSeatObj, disjointArrangement))
    ).getCurrentSatisfaction()
    if nonDisjointArrangement:
      nonDisjointSatisfaction = Group(
        group.code, 
        group.numberOfReservations, 
        len(groups), 
        list(map(convertIndexToSeatObj, nonDisjointArrangement))
      ).getCurrentSatisfaction()
    else:
      nonDisjointSatisfaction = 0

    if disjointSatisfaction > nonDisjointSatisfaction:
      group.assignedSeats = list(map(convertIndexToSeatObj, disjointArrangement))
      occupySeats(availableSeats, disjointArrangement)
    else:
      group.assignedSeats = list(map(convertIndexToSeatObj, nonDisjointArrangement))
      occupySeats(availableSeats, nonDisjointArrangement)


  with open("result.txt", "w") as f:
    for group in groups:
      f.write(group.code + " " + group.getSeatArrangementString() + "\n")

  print(os.path.abspath("result.txt"))


if __name__ == '__main__':
  # if no command line args are passed then just take 'input_file.txt' 
  # as the default path to the data file
  path = "input_file.txt" if len(sys.argv) < 2 else sys.argv[1]
  main(path)

