#define CLK 2       // Rotary Encoder Clock (A)
#define DT 3        // Rotary Encoder Data (B)
#define SW 4        // Rotary Encoder Button (Mute)
#define DS1802_CLK 6  // DS1802 Clock
#define DS1802_UD 7   // DS1802 Up/Down
#define DS1802_MUTE 5 // DS1802 Mute

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
}

void loop() {
    // Read encoder button (mute toggle)
    if (digitalRead(SW) == LOW) {
        delay(50); // Debounce
        if (digitalRead(SW) == LOW) {
            muteState = !muteState;
            digitalWrite(DS1802_MUTE, muteState ? LOW : HIGH);
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }

    // Check if encoder is rotated
    int encoderState = digitalRead(CLK);
    if (encoderState != lastEncoderState) {
        if (digitalRead(DT) != encoderState) {
            if (balanceMode) balance = constrain(balance + 1, -10, 10);  // Increase balance right
            else volume = constrain(volume + 1, 0, 63);  // Increase volume
        } else {
            if (balanceMode) balance = constrain(balance - 1, -10, 10);  // Increase balance left
            else volume = constrain(volume - 1, 0, 63);  // Decrease volume
        }

        updateVolume();
        lastEncoderState = encoderState;
    }

    // Hold button to switch to balance mode
    if (digitalRead(SW) == LOW) {
        delay(500);  // Long press detection
        if (digitalRead(SW) == LOW) {
            balanceMode = !balanceMode; // Toggle balance mode
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }
}

// Function to update DS1802 volume levels
void updateVolume() {
    int leftVol = volume + (balance < 0 ? balance : 0);  // Reduce left if balance < 0
    int rightVol = volume - (balance > 0 ? balance : 0); // Reduce right if balance > 0

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
