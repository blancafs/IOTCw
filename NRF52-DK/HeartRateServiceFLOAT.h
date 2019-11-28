#ifndef __BLE_HEART_RATE_SERVICE_H__
#define __BLE_HEART_RATE_SERVICE_H__

#include "ble/BLE.h"
#include <UUID.h>


/**
* @class HeartRateService
* @brief BLE Service for HeartRate. This BLE Service contains the location of the sensor and the heart rate in beats per minute.
* Service:  https://developer.bluetooth.org/gatt/services/Pages/ServiceViewer.aspx?u=org.bluetooth.service.heart_rate.xml
* HRM Char: https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml
* Location: https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.body_sensor_location.xml
*/
class HeartRateService {
public:
    /**
    * @enum SensorLocation
    * @brief Location of the heart rate sensor on body.
    */
    enum {
        LOCATION_OTHER = 0, /*!< Other location. */
        LOCATION_CHEST,     /*!< Chest. */
        LOCATION_WRIST,     /*!< Wrist. */
        LOCATION_FINGER,    /*!< Finger. */
        LOCATION_HAND,      /*!< Hand. */
        LOCATION_EAR_LOBE,  /*!< Earlobe. */
        LOCATION_FOOT,      /*!< Foot. */
    };

public:
    /**
     * @brief Constructor with 8-bit HRM Counter value.
     *
     * @param[ref] _ble
     *               Reference to the underlying BLE.
     * @param[in] hrmCounter (8-bit)
     *               Initial value for the HRM counter.
     * @param[in] location
     *               Sensor's location.
     */
     /* generating correct uuid */
    UUID customCharacteristicUUID = UUID("ef680406-9b35-4933-9b10-52ffa9740042");
    unsigned max_size = 4;
    HeartRateService(BLE &_ble, float hrmCounter, uint8_t location) :
        ble(_ble),
        valueBytes(hrmCounter),
        hrmRate(customCharacteristicUUID, valueBytes.getPointer(),
                valueBytes.getNumValueBytes(), max_size,
                GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_READ | GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        hrmLocation(GattCharacteristic::UUID_BODY_SENSOR_LOCATION_CHAR, &location),
        controlPoint(GattCharacteristic::UUID_HEART_RATE_CONTROL_POINT_CHAR, &controlPointValue) {
        setupService();
    }

    /**
     * @brief Constructor with a 16-bit HRM Counter value.
     *
     * @param[in] _ble
     *               Reference to the underlying BLE.
     * @param[in] hrmCounter (8-bit)
     *               Initial value for the HRM counter.
     * @param[in] location
     *               Sensor's location.
     */
    HeartRateService(BLE &_ble, uint8_t hrmCounter, uint8_t location) :
        ble(_ble),
        valueBytes(hrmCounter),
        hrmRate(GattCharacteristic::UUID_HEART_RATE_MEASUREMENT_CHAR, valueBytes.getPointer(),
                valueBytes.getNumValueBytes(), HeartRateValueBytes::MAX_VALUE_BYTES,
                GattCharacteristic::BLE_GATT_CHAR_PROPERTIES_NOTIFY),
        hrmLocation(GattCharacteristic::UUID_BODY_SENSOR_LOCATION_CHAR, &location),
        controlPoint(GattCharacteristic::UUID_HEART_RATE_CONTROL_POINT_CHAR, &controlPointValue) {
        setupService();
    }

    /**
     * @brief Set a new 8-bit value for the heart rate.
     *
     * @param[in] hrmCounter
     *                  Heart rate in BPM.
     */
    void updateHeartRate(uint8_t hrmCounter) {
        valueBytes.updateHeartRate(hrmCounter);  
        ble.gattServer().write(hrmRate.getValueHandle(), valueBytes.getPointer(), valueBytes.getNumValueBytes());
    }
    
    void updateHeartRate(float hrmCounter) {
        valueBytes.updateHeartRate(hrmCounter);  
        ble.gattServer().write(hrmRate.getValueHandle(), valueBytes.getPointer(), valueBytes.getNumValueBytes());
    }

    /**
     * Set a new 16-bit value for the heart rate.
     *
     * @param[in] hrmCounter
     *                  Heart rate in BPM.
     */
    void updateHeartRateNN(float hrmCounter) {
        //valueBytes.updateHeartRate(hrmCounter);
        
        uint8_t      bytes[sizeof(float)];
        *(float*)(bytes) = hrmCounter;  // convert float to bytes
        
        unsigned size = 1;
        uint8_t fake_value = 55;
        uint8_t* ptr = &fake_value;
        
        
        static const unsigned VALUE_FORMAT_BITNUM = 0;
        static const uint8_t  VALUE_FORMAT_FLAG   = (1 << VALUE_FORMAT_BITNUM);
        
        // insert header
        uint8_t payload[size+1];
        payload[0] = VALUE_FORMAT_FLAG;

        // insert payload
        //memcpy(&(payload[1]), fake_value, size);
        payload[1] = fake_value;

        // send
        ble.gattServer().write(hrmRate.getValueHandle(), payload, size);
    }

    /**
     * This callback allows the heart rate service to receive updates to the
     * controlPoint characteristic.
     *
     * @param[in] params
     *     Information about the characterisitc being updated.
     */
    virtual void onDataWritten(const GattWriteCallbackParams *params) {
        if (params->handle == controlPoint.getValueAttribute().getHandle()) {
            /* Do something here if the new value is 1; else you can override this method by
             * extending this class.
             * @NOTE: If you are extending this class, be sure to also call
             * ble.onDataWritten(this, &ExtendedHRService::onDataWritten); in
             * your constructor.
             */
        }
    }

protected:
    void setupService(void) {
        GattCharacteristic *charTable[] = {&hrmRate, &hrmLocation, &controlPoint};
        GattService         hrmService(GattService::UUID_HEART_RATE_SERVICE, charTable, sizeof(charTable) / sizeof(GattCharacteristic *));

        ble.addService(hrmService);
        ble.onDataWritten(this, &HeartRateService::onDataWritten);
    }

protected:
    /* Private internal representation for the bytes used to work with the value of the heart rate characteristic. */
    struct HeartRateValueBytes {
        static const unsigned MAX_VALUE_BYTES  = 5; /* Flags, and up to two bytes for heart rate. */
        static const unsigned FLAGS_BYTE_INDEX = 0;

        static const unsigned VALUE_FORMAT_BITNUM = 0;
        static const uint8_t  VALUE_FORMAT_FLAG   = (1 << VALUE_FORMAT_BITNUM);

        HeartRateValueBytes(uint8_t hrmCounter) : valueBytes() {
            updateHeartRate(hrmCounter);
        }

        HeartRateValueBytes(float hrmCounter) : valueBytes() {
            updateHeartRate(hrmCounter);
        }

        void updateHeartRate(uint8_t hrmCounter) {
            valueBytes[FLAGS_BYTE_INDEX]    &= ~VALUE_FORMAT_FLAG;
            valueBytes[FLAGS_BYTE_INDEX + 1] = hrmCounter;
        }

        void updateHeartRate(float hrmCounter) {
            uint8_t hrmCounterTEST = 33;
            
            uint8_t *array;
            //array = (unit8_t*)(&hrmCounter);
            
            valueBytes[FLAGS_BYTE_INDEX]    |= VALUE_FORMAT_FLAG;
            valueBytes[FLAGS_BYTE_INDEX + 1] = 0xFF;
            valueBytes[FLAGS_BYTE_INDEX + 2] = 0x00;
            valueBytes[FLAGS_BYTE_INDEX + 3] = 0xFF;
            valueBytes[FLAGS_BYTE_INDEX + 4] = 0x00;
            
//            valueBytes[FLAGS_BYTE_INDEX]    |= VALUE_FORMAT_FLAG;

//            valueBytes[FLAGS_BYTE_INDEX + 1] = (uint8_t)(hrmCounter & 0xFF);
//            valueBytes[FLAGS_BYTE_INDEX + 2] = (uint8_t)(hrmCounter >> 8);
        }

        uint8_t       *getPointer(void) {
            return valueBytes;
        }

        const uint8_t *getPointer(void) const {
            return valueBytes;
        }

        unsigned       getNumValueBytes(void) const {
            return 1 + 4;//((valueBytes[FLAGS_BYTE_INDEX] & VALUE_FORMAT_FLAG) ? sizeof(uint32_t) : sizeof(uint8_t));
        }

    private:
        /* First byte: 8-bit values, no extra info. Second byte: uint8_t HRM value */
        /* See https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml */
        uint8_t valueBytes[MAX_VALUE_BYTES];
    };

protected:
    BLE                 &ble;

    HeartRateValueBytes  valueBytes;
    uint8_t              controlPointValue;

    GattCharacteristic                   hrmRate;
    ReadOnlyGattCharacteristic<uint8_t>  hrmLocation;
    WriteOnlyGattCharacteristic<uint8_t> controlPoint;
};

#endif /* #ifndef __BLE_HEART_RATE_SERVICE_H__*/
