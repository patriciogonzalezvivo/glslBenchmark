
USER := profiler
HOST := raspberrypi.local

BENCHMARK_CMD := scripts/run.py

ifneq ("$(file)","")
BENCHMARK_CMD += $(file)
endif

all: remote_benchmark copy_to_local

clean: 
	rm -rf tests/*.png
	rm -rf tests/*.csv

install_keys:
	@cat ~/.ssh/id_rsa.pub | ssh $(USER)@$(HOST) 'cat >> .ssh/authorized_keys'

benchmark: remote_benchmark copy_to_local

remote_benchmark:
	@echo "Running benchmark.py script in REMOTE host $(HOST)"
	@rsync -ru --progress --delete ./ $(USER)@$(HOST):~/glslBenchmark
	@ssh $(USER)@$(HOST) 'cd ~/glslBenchmarks && make local_benchmark'

local_benchmark:
	@echo "Running benchmark.py script in LOCAL host"
	@python $(BENCHMARK_CMD)

copy_to_local:
	@echo "Copying benchmark results from $(HOST) back to local"
	@rsync -ru --progress $(USER)@$(HOST):~/glslBenchmark .

