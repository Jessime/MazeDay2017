import sys
import wave

in_fn = sys.argv[1]
out_fn = sys.argv[2]
num_seconds = float(sys.argv[3])

in_file = wave.open(in_fn,"r")
out_file = wave.open(out_fn,"w")
in_params = in_file.getparams()
out_file.setparams(in_params)
frame_rate = in_file.getframerate()
out_frames = int(frame_rate*num_seconds)
out_file.setnframes(out_frames)
out_file.writeframes(in_file.readframes(out_frames))

in_file.close()
out_file.close()

