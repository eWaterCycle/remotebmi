using Test
import RemoteBMI
import OpenAPI
using RemoteBMI.NonFinite: encode, decode

@testset "IEEE number conversion" begin
  for value in (NaN, Inf, -Inf, Float32(NaN), Float32(Inf), Float32(-Inf))
    @test isequal(decode(encode(value)), Float64(value))
  end
  for value in (0, 2^53 + 1, 1.25, Float32(1.25), -0.0)
    @test encode(value) === value
    @test decode(value) === value
  end
  @test_throws ArgumentError decode("invalid")
end

@testset "IEEE model field types" begin
  for models in (RemoteBMI.Client.BmiClient, RemoteBMI.Server.BmiServer)
    for name in (:IEEENumber, :IEEEDouble, :IEEEDoubleNoNaN)
      model = getproperty(models, name)
      valid = name == :IEEEDoubleNoNaN ? (1.25, "Infinity", "-Infinity") : (1.25, "NaN", "Infinity", "-Infinity")
      for value in valid
        @test model(value).value === value
        @test OpenAPI.from_json(model(), :value, value).value === value
        @test OpenAPI.from_json(model(), :value, value; stylectx = nothing).value === value
        @test OpenAPI.from_json(model(), value).value === value
        instance = model(0.0)
        instance.value = value
        @test instance.value === value
      end
      invalid = ("invalid", "nan", "Inf", "1.0", "", true, false, NaN, Inf, -Inf)
      if name == :IEEEDoubleNoNaN
        invalid = (invalid..., "NaN")
      end
      for value in invalid
        @test_throws ArgumentError model(value)
        @test_throws ArgumentError OpenAPI.from_json(model(), :value, value)
        @test_throws ArgumentError OpenAPI.from_json(model(), :value, value; stylectx = nothing)
        @test_throws ArgumentError OpenAPI.from_json(model(), value)
        instance = model(1.0)
        @test_throws ArgumentError instance.value = value
        @test instance.value === 1.0
      end
      for value in (nothing, [1.0], Dict("value" => 1.0), 1 + 2im)
        @test_throws MethodError model(value)
      end
    end
    @test models.IEEENumber(2^53 + 1).value === 2^53 + 1
    for name in (:IEEEDouble, :IEEEDoubleNoNaN)
      model = getproperty(models, name)
      @test model(1).value === 1.0
      @test OpenAPI.from_json(model(), :value, 1).value === 1.0
    end
  end
end
