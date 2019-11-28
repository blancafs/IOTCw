/* mbed Microcontroller Library
 * Copyright (c) 2006-2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <events/mbed_events.h>
#include <mbed.h>
#include "ble/BLE.h"
#include <time.h>
#include "ble/gap/Gap.h"
//#include "ble/services/HeartRateService.h"
#include "HeartRateService.h"
#include "pretty_printer.h"
#include "MPU9250/MPU9250.h"


const static char DEVICE_NAME[] = "Heartrate";
// Sensor board library
MPU9250 mpu = MPU9250(p26, p27);
Serial pc(USBTX, USBRX);
long counter = 0;

//uint16_t buffer[15];
//
//static events::EventQueue event_queue(/* event count */ 16 * EVENTS_EVENT_SIZE);
//
//class HeartrateDemo : ble::Gap::EventHandler {
//public:
//    HeartrateDemo(BLE &ble, events::EventQueue &event_queue) :
//        _ble(ble),
//        _event_queue(event_queue),
//        _led1(LED1, 1),
//        _connected(false),
//        _hr_uuid(GattService::UUID_HEART_RATE_SERVICE),
//        _hr_counter(100),
//        _hr_service(ble, _hr_counter, HeartRateService::LOCATION_FINGER),
//        _adv_data_builder(_adv_buffer) { }
//
//    void start() {
//        _ble.gap().setEventHandler(this);
//
//        _ble.init(this, &HeartrateDemo::on_init_complete);
//
//        _event_queue.call_every(500, this, &HeartrateDemo::blink);
//        //_event_queue.call_every(5, this, &HeartrateDemo::update_sensor_value);
//
//        _event_queue.dispatch_forever();
//    }
//
//private:
//    /** Callback triggered when the ble initialization process has finished */
//    void on_init_complete(BLE::InitializationCompleteCallbackContext *params) {
//        if (params->error != BLE_ERROR_NONE) {
//            printf("Ble initialization failed.");
//            return;
//        }
//
//        print_mac_address();
//
//        start_advertising();
//    }
//
//    void start_advertising() {
//        /* Create advertising parameters and payload */
//
//        ble::AdvertisingParameters adv_parameters(
//            ble::advertising_type_t::CONNECTABLE_UNDIRECTED,
//            ble::adv_interval_t(ble::millisecond_t(90)) //was 1000
//        );
//
//        _adv_data_builder.setFlags();
//        _adv_data_builder.setAppearance(ble::adv_data_appearance_t::GENERIC_HEART_RATE_SENSOR);
//        _adv_data_builder.setLocalServiceList(mbed::make_Span(&_hr_uuid, 1));
//        _adv_data_builder.setName(DEVICE_NAME);
//
//        /* Setup advertising */
//
//        ble_error_t error = _ble.gap().setAdvertisingParameters(
//            ble::LEGACY_ADVERTISING_HANDLE,
//            adv_parameters
//        );
//
//        if (error) {
//            printf("_ble.gap().setAdvertisingParameters() failed\r\n");
//            return;
//        }
//
//        error = _ble.gap().setAdvertisingPayload(
//            ble::LEGACY_ADVERTISING_HANDLE,
//            _adv_data_builder.getAdvertisingData()
//        );
//
//        if (error) {
//            printf("_ble.gap().setAdvertisingPayload() failed\r\n");
//            return;
//        }
//
//        /* Start advertising */
//
//        error = _ble.gap().startAdvertising(ble::LEGACY_ADVERTISING_HANDLE);
//
//        if (error) {
//            printf("_ble.gap().startAdvertising() failed\r\n");
//            return;
//        }
//    }
//
//    void update_sensor_value() {
//        if (_connected) {
//            // Do blocking calls or whatever is necessary for sensor polling.
//            // In our case, we simply update the HRM measurement.
//           // _hr_counter++;
//
//            //  100 <= HRM bps <=175
//            //if (_hr_counter == 175) {
////                _hr_counter = 100;
////            }
//            //float _hr_float_counter = 12.0;
//            uint16_t mag[3];
//            //mag[0] = 2;
////            mag[1] = 3;
//
//
//            int16_t accelerometer[3] = {0,0,0};
//            //int16_t gyroscope[3] = {0,0,0};
//            mpu.readAccelData(accelerometer);
//            float ax = accelerometer[0] * 2.0 / 32768.0;
//            float ay = accelerometer[1] * 2.0 / 32768.0;
//            float az = accelerometer[2] * 2.0 / 32768.0;
//            
//            //float magnitude = sqrt((ax*ax) + (ay*ay) + (az*az));
////            
////            uint16_t ax_test = floor((ax * 10000.0) + 0.5);
////            uint16_t ay_test = floor((ay * 10000.0) + 0.5);
////            uint16_t az_test = floor((az * 10000.0) + 0.5);
////            
////            uint16_t mag_test = floor((magnitude * 1000.0) + 0.5); //magnitude to send off
//            
//            
//            //add to array
//            //buffer[counter] = mag_test;
////            counter = counter+1;
//            
//            time_t now = time(NULL);
//            
//            pc.printf("%ld\n", now);
//            pc.printf("%f, %f, %f, %f\n", ax, ay, az, az); 
////            pc.printf("%u, %u, %u, %u\n", ax_test, ay_test, az_test, mag_test); 
////            pc.printf("Frequency: %f\n", (float)counter/((float)time(NULL)-(float)started)); 
//
//            
//            //if(counter>8){
////                counter = 0;
////                _hr_service.updateHeartRate(buffer);
////            }
//            
//        }
//    }
//
//    void blink(void) {
//        _led1 = !_led1;
//    }
//
//private:
//    /* Event handler */
//
//    void onDisconnectionComplete(const ble::DisconnectionCompleteEvent&) {
//        _ble.gap().startAdvertising(ble::LEGACY_ADVERTISING_HANDLE);
//        _connected = false;
//    }
//
//    virtual void onConnectionComplete(const ble::ConnectionCompleteEvent &event) {
//        if (event.getStatus() == BLE_ERROR_NONE) {
//            _connected = true;
//        }
//    }
//
//private:
//    BLE &_ble;
//    events::EventQueue &_event_queue;
//    DigitalOut _led1;
//
//    bool _connected;
//
//    UUID _hr_uuid;
//
//    uint8_t _hr_counter;
//    HeartRateService _hr_service;
//
//    uint8_t _adv_buffer[ble::LEGACY_ADVERTISING_MAX_SIZE];
//    ble::AdvertisingDataBuilder _adv_data_builder;
//};
//
///** Schedule processing of events from the BLE middleware in the event queue. */
//void schedule_ble_events(BLE::OnEventsToProcessCallbackContext *context) {
//    event_queue.call(Callback<void()>(&context->ble, &BLE::processEvents));
//}

int main()
{
    //BLE &ble = BLE::Instance();
    //ble.onEventsToProcess(schedule_ble_events);
    
    mpu.initMPU9250();
    wait(1);
    
    int counter = 0;
    
    while(true){
        
        int16_t accelerometer[3] = {0,0,0};
        mpu.readAccelData(accelerometer);
        float ax = accelerometer[0] * 2.0 / 32768.0;
        float ay = accelerometer[1] * 2.0 / 32768.0;
        float az = accelerometer[2] * 2.0 / 32768.0;
        counter=counter+1;
        int time_passed = counter*5;
                
        pc.printf("Time passed: %u ms\n", time_passed);
        pc.printf("%d\n", counter);
        pc.printf("%f, %f, %f, %f\n", ax, ay, az, az); 
        wait(0.005);
    
    }
    
    //HeartrateDemo demo(ble, event_queue);
    //demo.start();

    return 0;
}

