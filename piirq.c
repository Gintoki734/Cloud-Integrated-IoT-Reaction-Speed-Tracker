/*
 ============================================================================
 Name        : piirq.c
 Author      : Shreeharsha Khanal
 Version     : 0.5
 Copyright   : See Abertay copyright notice
 Description : RPi test to get value from python and do actions
 ============================================================================
 */
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/delay.h>

static unsigned int Led = 23;
static unsigned int Buzz = 25;
static unsigned int Irqnum = 0;

// getting data from the python and storing it
static int time = 0;
module_param(time, int, 0644);
MODULE_PARM_DESC(time, "Time the buzzer will stay on for");

static int led_state = 0;
module_param(led_state, int, 0644);
MODULE_PARM_DESC(led_state, "The state of the led depending on if MQTT is connected or not");

int __init piirq_init(void){
    pr_info("%s\n", __func__);
    //https://www.kernel.org/doc/Documentation/pinctrl.txt
	printk("piirq: IRQ Test");
    printk(KERN_INFO "piirq: Initializing driver\n");

    if (!gpio_is_valid(Led)||!gpio_is_valid(Buzz)){
    	printk(KERN_INFO "piirq: invalid GPIO\n");
    return -ENODEV;
   }
           // Initialize the LED GPIO
	   gpio_request(Led, "Led");
	   // Changes Led depending if it is connected to MQTT or not
	   gpio_direction_output(Led, led_state);
	   // Causes to appear in /sys/class/gpio/gpio16 for echo 0 > value
	   gpio_export(Led, false);
	   
	   // Initialize Buzzer GPIO
           gpio_request(Buzz, "Buzz");
    	   gpio_direction_output(Buzz, 0);
    	   gpio_export(Buzz, false);
    	   
    	   gpio_set_value(Buzz, 1);        // Turn on buzzer
	   msleep(time);                   // Buzz depending on the value of time
	   gpio_set_value(Buzz, 0);        // Turn off buzzer
    	   
    	   

    printk("piirq loaded\n");
    return 0;
}
void __exit piirq_exit(void){
   gpio_set_value(Led, 0); //start led in off state
   gpio_set_value(Buzz, 0); //start buzz in off state
   
   gpio_unexport(Led);
   gpio_unexport(Buzz);
   
   free_irq(Irqnum, NULL);
   gpio_free(Led);
   gpio_free(Buzz);
   printk("piirq unloaded\n");
}
module_init(piirq_init);
module_exit(piirq_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("SK");
MODULE_DESCRIPTION("RPi Mini Project");
MODULE_VERSION("0.5");
