<?php

class LoadOptions
{
    private $languages;
    private $encodings;

    public function __construct()
    {
        $this->languages = $this->load_languages();
        $this->encodings = $this->load_encodings();
    }

    public function get_languages()
    {
        return $this->languages;
    }

    public function get_encodings()
    {
        return $this->encodings;
    }

    private function load_languages()
    {
        $json_languages = file_get_contents('php_scripts/configs/languages.json');
        $json_languages = json_decode($json_languages, True);
        $json_languages = $json_languages['languages'];

        $languages = array();
        foreach ($json_languages as $document) {
            $option = $document['option'];
            $value = $document['value'];
            $languages[$option] = $value;
        }
        ksort($languages);

        return $languages;
    }

    private function load_encodings()
    {
        $json_encodings = file_get_contents('php_scripts/configs/encodings.json');
        $json_encodings  = json_decode($json_encodings , True);
        $json_encodings  = $json_encodings['encodings'];

        $encodings = array();
        foreach ($json_encodings as $document) {
            $option = $document['option'];
            $value = $document['value'];
            $encodings[$option] = $value;
        }
        ksort($encodings);

        return $encodings;
    }
}