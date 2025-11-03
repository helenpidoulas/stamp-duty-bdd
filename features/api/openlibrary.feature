Feature: Validate author details from OpenLibrary API

  @api @openlibrary
  Scenario: Verify personal_name and alternate_names for OL1A
    Given I fetch the author payload for "https://openlibrary.org/authors/OL1A.json"
    Then the JSON field "personal_name" should equal "Sachi Rautroy"
    And the JSON array "alternate_names" should contain "Yugashrashta\u202FSachi\u202FRoutray"
