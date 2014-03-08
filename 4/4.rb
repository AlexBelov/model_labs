require 'colored'
require 'json'

class Queue
  def initialize λ, μ1, μ2, max_queue_count_1, max_queue_count_2
    @λ = λ
    @phase1 = Phase.new(μ1, max_queue_count_1)
    @phase2 = Phase.new(μ2, max_queue_count_2)
    @denial_count_1 = 0
    @denial_count_2 = 0
    @denial_count = 0
    @requests_number = 0
    @requests_number_2 = 0
    @denial_probability_1 = 0
    @denial_probability_2 = 0
    @denial_probability = 0

    instance_variables.each do |var|
      eval "def #{var.to_s.sub('@','')}; #{var}; end"
    end
  end

  def imitate requests_number = 100_000
    @requests_number = requests_number
    request_stream = []
    current_time = 0
    request_stream.push 0
    requests_number.times do
      current_time += -Math.log(rand) / @λ
      request_stream.push current_time
    end

    request_stream_2 = @phase1.imitate request_stream
    stream = @phase2.imitate request_stream_2

    @requests_number_2 = request_stream_2.size
    @denial_count_1 = @phase1.denial_count
    @denial_count_2 = @phase2.denial_count
    @denial_count = @denial_count_1 + @denial_count_2
    @denial_probability_1 = @denial_count_1 / @requests_number.to_f
    @denial_probability_2 = @denial_count_2 / @requests_number_2.to_f
    @denial_probability = @denial_count / @requests_number.to_f
  end
end

class Phase
  def initialize μ, max_queue_count
    @μ = μ
    @max_queue_count = max_queue_count
    @denial_count = 0

    instance_variables.each do |var|
      eval "def #{var.to_s.sub('@','')}; #{var}; end"
    end
  end

  def imitate input_stream
    current_time = 0
    queue_count = 0
    denial_count = 0

    output_stream = []

    current_request = 0
    while current_request < input_stream.size
      if input_stream[current_request] < current_time
        if queue_count == @max_queue_count
          denial_count += 1
        else
          queue_count += 1
        end
        current_request += 1
      else
        if queue_count > 0
          current_time += -Math.log(rand) / @μ
          queue_count -= 1
        else
          current_time = input_stream[current_request] + -Math.log(rand) / @μ
          current_request += 1
        end
        output_stream.push current_time
      end
    end

    @denial_count = denial_count
    return output_stream
  end
end

q = Queue.new 5,5,5,2,2
q.imitate
puts "For λ = 5".cyan
puts "Potk1 = %5.5f".red % q.denial_probability_1
puts "Potk2 = %5.5f".red % q.denial_probability_2
puts "P = %5.5f".red % q.denial_probability

plot_data = []
denial_1 = []
denial_2 = []
denial = []

for λ in (1..6).step 0.5
  q = Queue.new λ,5,5,2,2
  q.imitate
  denial_1 << q.denial_probability_1
  denial_2 << q.denial_probability_2
  denial << q.denial_probability
end

plot_data << denial_1 << denial_2 << denial

File.open('plot_data.json','w') do |f|
  f.write plot_data.to_json
end

exec 'python draw_plot.py'
