all: run

run:
	@python main.py

profile:
	@python -m memory_profiler main.py

clean:
	@rm *.pyc
