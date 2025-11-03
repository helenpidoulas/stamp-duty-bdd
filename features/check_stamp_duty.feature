Feature: Check motor vehicle stamp duty via Service NSW -> Revenue NSW calculator

  @happy_path
  Scenario: Calculate duty for a passenger vehicle and validate popup
    Given I open the Service NSW "Check motor vehicle stamp duty" page
    When I click the Check online button
    Then I should land on the Revenue NSW motor vehicle duty calculator
    When I select "Yes" for passenger vehicle
    And I enter the vehicle amount
    And I click Calculate
    Then a popup should appear with the correct duty
