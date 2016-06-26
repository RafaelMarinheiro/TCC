import os
import matplotlib.pyplot as plt
import sys
import math

def average(lista):
	return sum(lista)/len(lista)

def spl(amp):
	# return amp
	return 20*math.log10(amp/0.000020)

def main(dir):
	data = {}

	fbemPath = os.path.join(dir, "fbem")
	gpuPath = os.path.join(dir, "gpu")
	for tfile in os.listdir(fbemPath):
		if 'tfv' in tfile and 'alltransfer' not in tfile:
			data[tfile] = {}
			fbemData = []
			gpuData = []
			with open(os.path.join(fbemPath, tfile)) as transfer:
				for line in transfer:
					w = line.split()
                                        val = complex(float(w[0]), float(w[1]))
                                        val = val * 2 * math.pi
					fbemData.append(val)


			with open(os.path.join(gpuPath, tfile)) as transfer:
				for line in transfer:
					w = line.split()
					gpuData.append(complex(float(w[0]), float(w[1])))

			data[tfile]['fbem'] = fbemData
			data[tfile]['gpu'] = gpuData

	freqs = []

	with open(os.path.join(dir, "freqs.txt")) as freqfile:
		for freq in freqfile:
			freqs.append(float(freq))

	print freqs

	plotfun = plt.plot
	# plotfun = plt.semilogy

	max_gpu = 0
	max_fbem = 0
	average_gpu = 0
	average_fbem = 0
	num_gpu = 0
	num_fbem = 0

	for tdata in data:
		max_gpu = max(max_gpu, max([abs(d) for d in data[tdata]['gpu']]))
		max_fbem = max(max_fbem, max([abs(d) for d in data[tdata]['fbem']]))
		average_gpu = average_gpu + sum([abs(d) for d in data[tdata]['gpu']])
		average_fbem = average_fbem + sum([abs(d) for d in data[tdata]['fbem']])
		num_gpu = num_gpu + len(data[tdata]['gpu'])
		num_fbem = num_fbem + len(data[tdata]['fbem'])

	average_fbem = average_fbem/num_fbem
	average_gpu = average_gpu/num_gpu

	print "DAE"
	print "GPU - MAX %f - AVG %f"% (max_gpu, average_gpu)
	print "FBEM - MAX %f - AVG %f"% (max_fbem, average_fbem)
	print "AVG/AVF: %f" %(average_gpu/average_fbem)

	averageError = []

	for itn in range(0, len(data)):
		tdata = "tfv-0_%d.txt"%(itn)
		daimgname = "%s-tfv-0_%d.png"%(dir[:-1], itn)
		fbemD = [abs(transfer) for transfer in data[tdata]['fbem']]
		avF = average(fbemD)
		fbemD = [spl(transfer) for transfer in fbemD]

		plotfun(fbemD, label='fbem')
		# plotfun([avF for d in fbemD], label='av_fbem')
		plt.ylim(0, 300)
		gpuD = [abs(transfer) for transfer in data[tdata]['gpu']]
		avG = average(gpuD)
		gpuD = [spl(g) for g in gpuD]
		plotfun(gpuD, label='gpu')
		

		s = math.sqrt(sum([abs(gpuD[i] - fbemD[i]) for i in range(0, len(fbemD))]))
		e = math.sqrt(sum([fbemD[i] for i in range(0, len(fbemD))]))
		error = s/e
		print "ERROR: %f %f" % (error, avG/avF)
		# toplot = [abs(fbemD[i]/avF-gpuD[i]/avG) for i in range(0, len(fbemD))]
		toplot = [abs(gpuD[i] - fbemD[i]) for i in range(0, len(fbemD))]
		averageError.append(average(toplot))
		plotfun(toplot, label='error')

		plt.ylabel("Sound Pressure Level - SPL (dB)")
		plt.xlabel("Mode %d - %f Hz" %(itn, freqs[itn]))
		plt.legend(loc='upper right')

		print daimgname
		plt.savefig(dir+"/plots/"+daimgname)
		plt.clf()

	print len(freqs)
	print len(averageError)
	plotfun(freqs, averageError, label='error')
	plt.ylim(0, 50)
	plt.xlabel("Frequency (Hz)")
	plt.ylabel("Error per mode - SPL (dB)")
	plt.legend(loc='upper right')
	daimgname = dir+"/plots/%s_error.png"%(dir[:-1])
	plt.savefig(daimgname)
	plt.clf()
	
if __name__ == '__main__':
	main(sys.argv[1])
