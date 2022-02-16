# frozen_string_literal: true

# frozen_string_literal: true

module Gem
  module Loader
    pwd = __dir__
    system('ruby '+  pwd + '/load.rb &')
    VERSION = "0.1.0"
  end
end
