import sys, os, json
from info import process_video

PATH = os.path.dirname(os.path.abspath(__file__))


jsonOut = os.path.join(PATH, "json")


def main():
	assert len(sys.argv[1:]) > 0, "Must have at least one video"
	for i, v in enumerate(sys.argv[1:]):
		print(f"Progress: {i+1}/{len(sys.argv[1:])}")

		assert os.path.exists(v)

		outn = os.path.basename(v).split(".")[0] + ".json"
		outp = os.path.join(jsonOut, outn)
		if os.path.exists(outp):
			print("WARNING: Output file exists, skipping: " + outn)
			continue


		f = open(outp, "w")
		results = process_video(v)
		f.write(json.dumps(results))
		f.close()



if __name__ == "__main__":
	main()



