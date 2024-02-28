import csv
import time
import numpy

def read_data_file(real_time: bool = False) -> tuple:
	"""Generator function that returns data from data.csv file.

	Parameters:
		real_time: Enable real time data reading by adding a 10 ms pause between each data

	Returns:
		t: timestamp in millisecond.
		x: horizontal position in pixel.
		y: vertical position in pixel.
	"""

	with open('data.csv') as csv_file:

		csv_reader = csv.reader(csv_file, delimiter= ',')

		# Ignore header
		next(csv_reader)

		# Read data
		for data in csv_reader:

			# Unpack data
			t, x, y = float(data[0]), float(data[1]), float(data[2])

			# Edit millisecond timestamp
			t = int(round(t * 1e3))

			# Edit pixel positions
			x, y = int(x), int(y)

			# Return data
			yield t, x, y

			# Pause reading if required
			if real_time:

				time.sleep(0.01)

def calculate_centroid_deviation(txy_list: list) -> float:
	"""Calculate the centroid and the maximal deviation from a list of (t, x, y) elements.

	Returns:
		centroid: the centroid of incoming list
		deviation_max: the maximal deviation from incoming list.
	"""

	positions_array = numpy.asarray(txy_list)[:,1:]
	centroid = numpy.mean(positions_array, axis=0)
	deviations_array = numpy.sqrt(numpy.sum((positions_array - centroid)**2, axis=1))

	return centroid, deviations_array.max()

def load_aoi_file() -> dict:
	"""Returns all aoi from aoi.csv file.

	Returns:
		aois: dictionary where keys are aoi names and values are aoi bounding boxes (lower horizontal value, lower vertical value, upper horizontal value, upper horizontal value).
	"""

	with open('aoi.csv') as csv_file:

		csv_reader = csv.reader(csv_file, delimiter= ',')

		# Read aoi
		aois = {}
		for aoi in csv_reader:

			# Unpack aoi
			aois[str(aoi[0])] = (int(aoi[1]), int(aoi[2]), int(aoi[3]), int(aoi[4]))

		return aois
