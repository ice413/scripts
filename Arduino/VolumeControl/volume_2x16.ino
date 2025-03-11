#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define CLK 2       // Rotary Encoder Clock (A)
#define DT 3        // Rotary Encoder Data (B)
#define SW 4        // Rotary Encoder Button (Mute)
#define DS1802_CLK 6  // DS1802 Clock
#define DS1802_UD 7   // DS1802 Up/Down
#define DS1802_MUTE 5 // DS1802 Mute

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Adjust 0x27 to your LCD's I2C address

bool muteState = false;
int volume = 15;  // Initial volume (0-63)
int balance = 0;  // Balance (-10 to 10)
bool balanceMode = false;
int lastEncoderState;

void setup() {
    pinMode(CLK, INPUT_PULLUP);
    pinMode(DT, INPUT_PULLUP);
    pinMode(SW, INPUT_PULLUP);
    pinMode(DS1802_CLK, OUTPUT);
    pinMode(DS1802_UD, OUTPUT);
    pinMode(DS1802_MUTE, OUTPUT);

    digitalWrite(DS1802_MUTE, HIGH);  // Start unmuted
    lastEncoderState = digitalRead(CLK);

    // Initialize LCD
    lcd.init();
    lcd.backlight();
    updateLCD();
}

void loop() {
    // Read encoder button (mute toggle)
    if (digitalRead(SW) == LOW) {
        delay(50); // Debounce
        if (digitalRead(SW) == LOW) {
            muteState = !muteState;
            digitalWrite(DS1802_MUTE, muteState ? LOW : HIGH);
            updateLCD();
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }

    // Check if encoder is rotated
    int encoderState = digitalRead(CLK);
    if (encoderState != lastEncoderState) {
        if (digitalRead(DT) != encoderState) {
            if (balanceMode) balance = constrain(balance + 1, -10, 10);
            else volume = constrain(volume + 1, 0, 63);
        } else {
            if (balanceMode) balance = constrain(balance - 1, -10, 10);
            else volume = constrain(volume - 1, 0, 63);
        }

        updateVolume();
        updateLCD();
        lastEncoderState = encoderState;
    }

    // Hold button to switch to balance mode
    if (digitalRead(SW) == LOW) {
        delay(500);  // Long press detection
        if (digitalRead(SW) == LOW) {
            balanceMode = !balanceMode;
            updateLCD();
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }
}

// Function to update DS1802 volume levels
void updateVolume() {
    int logVolume = pow(10, (volume / 63.0) * log10(63)); // Logarithmic mapping

    int leftVol = logVolume + (balance < 0 ? balance : 0);
    int rightVol = logVolume - (balance > 0 ? balance : 0);

    sendToDS1802(leftVol);
    sendToDS1802(rightVol);
}

// Function to send volume to DS1802
void sendToDS1802(int vol) {
    for (int i = 0; i < 7; i++) {
        digitalWrite(DS1802_CLK, LOW);
        digitalWrite(DS1802_UD, (vol & (1 << i)) ? HIGH : LOW);
        digitalWrite(DS1802_CLK, HIGH);
    }
}

// Function to update the LCD display
void updateLCD() {
    lcd.clear();

    // Line 1: Display Volume or MUTE
    if (muteState) {
        lcd.setCursor(0, 0);
        lcd.print("MUTE");
    } else {
        lcd.setCursor(0, 0);
        lcd.print("Volume: ");
        lcd.print(volume);
        lcd.print("dB");
    }

    // Line 2: Display Balance
    lcd.setCursor(0, 1);
    if (balanceMode) {
        lcd.print("Balance Mode ");
    } else {
        lcd.print("L");
        int barPos = map(balance, -10, 10, 1, 14);
        for (int i = 1; i < 15; i++) {
            if (i == barPos) lcd.print("|");  // Center mark
            else lcd.print("-");
        }
        lcd.print("R");
    }
}