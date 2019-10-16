# Sphero SDK

Greetings adventurous students, developers, hackers, and makers!  RVR is one of the best starting points into the vast world of robotics, and we’re here to help you get started with using our approachable development tools.

## First things first

### Getting Started

Visit our [Getting Started](https://sdk.sphero.com/getting_started) to learn more about the ins-and-outs of working with RVR, including some important details on the getting started process.

### More information and documentation

Visit our [SDK website](https://sdk.sphero.com) to find more information about RVR, the SDK and the API!

### Where to get help

Visit our [community forum](https://community.sphero.com/c/advanced-programming) to get help, share your project, or help others!

### Staying up to date

Consider [signing up](https://sdk.sphero.com/sign-up) for our SDK email list to stay current on new features being released in our robot firmware as well as our SDKs, including new platform / language support.  

## About the Raspberry Pi Python SDK

Our SDK is meant for beginners and experts alike. If you are just getting started on your journey, and would like some helpful guides on using RVR’s features, you can find plenty of examples in our `getting_started` directory.  The RVR SDK comes in two formats: `asyncio` and `observer`. You’ll notice our `getting_started` samples are divided into two subdirectories of the same name.  Before we get into specifying the difference between the two, we’d like to point out both subdirectories feature the same types of examples, but with slightly different syntax.

Who should use the `asyncio` version of the SDK? If you consider your python skills mid-to-advanced-level, and have experience with asynchronous programming, then you might feel at home with this version.  As the name suggests, it uses the publicly available `asyncio` library under the hood to send and receive data from RVR.  Asynchronously programming RVR becomes relevant when you start hooking up external input devices to your Raspberry-Pi, and need additional third-party libraries to operate them.  Often times the code to get input data from an external device halts execution of a program until the data is acquired.  You’ll likely want your code to continue executing in parallel, instead of waiting for the device code to finish executing.  Another great feature of the `asyncio` version is it enables users to communicate with RVR using the REST API.   This means you can control RVR over the web!  We’ve included samples using both the serial port, and the REST API for your convenience.

If you consider yourself a beginner, we recommend using the `observer` version of our SDK.  If you plan working primarily with a stand-alone Raspberry-Pi and RVR, this will be a good way to gain experience, without the overhead of learning the nuances of asynchronous programming.  The name `observer` refers to the the software design principle implemented in that version of the SDK.  In a nutshell, RVR is the “observer” of the data being written and read from serial port, and dispatches “events” that your code is listening for, typically in the form of callback functions referred to as “handlers”.  Since this version of the SDK is not asynchronous, interfacing with external devices, third-party libraries, or other sections of your program that halt execution until input is received will also block communication with RVR.  This could result in noticeable pauses in RVR’s operation at runtime.

The best way to get familiar with either version of our SDK is to dive into the `getting_started` samples, and follow along with code.  Feel free to modify the programs and experiment to gain a better understanding of what different values, and inputs affect the operation of RVR.  If you find yourself needing assistance, we are always happy to provide help through our community portal where other Sphero enthusiasts, as well as our developers can share knowledge, and help you succeed with your ideas.

Happy coding!
