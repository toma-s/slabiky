<?php

class Test
{
    function __construct($test_name, $real_value, $expected_value)
    {
        $this->test_name = $test_name;
        $this->real_value = $real_value;
        $this->expected_value = $expected_value;
    }

    function evaluate()
    {
        if ($this->real_value === $this->expected_value) {
            echo "Test $this->test_name was sucessful.\n\r";
        } else {
            "Test $this->test_name wasn`t sucessful.\n\r
             Expected: $this->expected_value\n\r
             Got: $this->real_value\n\r";
        }
    }
}