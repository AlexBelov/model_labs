require 'colored'

class Generator
  def initialize
    @pi1 = ARGV[0].to_f
    @pi2 = ARGV[1].to_f
    @cycles = ARGV[2].to_f

    @pi1 = 0.6 if @pi1 <= 0 or @pi1 > 1.0
    @pi2 = 0.5 if @pi2 <= 0 or @pi2 > 1.0
    @cycles = 10000 if @cycles < 1 or @pi2 > 1e7

    @cycles_berore_request = 2
    @queue = 0
    @service_1 = 0
    @service_2 = 0

    @services_count = 0
    @queue_processed = 0

    @log = File.open("logfile.txt", "w")
    @log.puts "2000"

    @states = { "2000" => 0,
                "1000" => 0,
                "2010" => 0,
                "1010" => 0,
                "2011" => 0,
                "1001" => 0,
                "1011" => 0,
                "2111" => 0,
                "1111" => 0,
                "2211" => 0,
                "1211" => 0
              }
  end

  def no_service_1
    rand < @pi1
  end

  def no_service_2
    rand < @pi2
  end

  def request?
    @cycles_berore_request -= 1
    if @cycles_berore_request == 0
      @cycles_berore_request = 2
      return true
    end
    return false
  end

  def count_states
    @states["#{@cycles_berore_request}#{@queue}#{@service_1}#{@service_2}"] += 1
  end

  def generate_new_state

    if @service_1 == 1
      if no_service_1
      else
        @service_1 = 0
      end
    end

    if @service_2 == 1
      if no_service_2
      else
        @service_2 = 0
      end
    end

    if @queue > 0
      if @service_1 == 0 and @service_2 == 1
        @queue -= 1
        @service_1 = 1
      elsif @service_1 == 1 and @service_2 == 0
        @queue -= 1
        @service_2 = 1
      elsif @service_1 == 0 and @service_2 == 0
        if @queue == 2
          @service_1 = 1
          @service_2 = 1
          @queue = 0
        elsif @queue == 1
          @service_1 = 1
          @queue = 0
        end
      end
    end

    unless request?
      @log.puts "#{@cycles_berore_request}#{@queue}#{@service_1}#{@service_2}"
      count_states
      @queue_processed += @queue
      @services_count = @services_count + @service_1 + @service_2
      return
    end

    if @queue == 0
      if @service_1 == 0
        @service_1 = 1
      elsif @service_2 == 0
        @service_2 = 1
      else
        @queue += 1
      end
    elsif @queue == 2
      return
    elsif @queue == 1
      @queue += 1
    end

    @log.puts "#{@cycles_berore_request}#{@queue}#{@service_1}#{@service_2}"
    count_states
    @queue_processed += @queue
    @services_count = @services_count + @service_1 + @service_2

  end

  def run
    @cycles.to_i.times do 
      generate_new_state
    end

    puts "System performance metrics".green
    puts "Average queue length per cycle: ".red + "#{@queue_processed/@cycles.to_f}".cyan
    puts "Average requests processed per cycle: ".red + "#{@services_count/@cycles.to_f}".cyan
    puts "States probabilities".green
    @states.each do |state, count|
      puts "P#{state}".red + "=" + " #{count/@cycles.to_f}".cyan
    end
  end

end

generator = Generator.new
generator.run
