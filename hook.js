function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function hook_android_dlopen_ext() {
    var linker64_base_addr = Module.getBaseAddress("linker64")
    var android_dlopen_ext_func_off = 0x0000000000014448
    var android_dlopen_ext_func_addr = linker64_base_addr.add(android_dlopen_ext_func_off)
    Interceptor.attach(android_dlopen_ext_func_addr, {
        onEnter: function (args) {
            // console.log("android_dlopen_ext -> enter : " + args[0].readCString())
            if (args[0].readCString() != null && args[0].readCString().indexOf("libmsaoaidsec.so") >= 0) {
                hook_call_constructors()
            }
        },
        onLeave: function (ret) {
            // console.log("android_dlopen_ext -> leave")
        }
    })
}

function hook_call_constructors() {
    var linker64_base_addr = Module.getBaseAddress("linker64")
    var call_constructors_func_off = 0x000000000002C2AC
    var call_constructors_func_addr = linker64_base_addr.add(call_constructors_func_off)
    var listener = Interceptor.attach(call_constructors_func_addr, {
        onEnter: function (args) {
            console.log("call_constructors -> enter")
            var module = Process.findModuleByName("libmsaoaidsec.so")
            if (module != null) {
                Interceptor.replace(module.base.add(0x000000000001BEC4), new NativeCallback(function () {
                    console.log("replace sub_1BEC4")
                }, "void", []))
                listener.detach()
            }
        },
    })
}

function hook_3des_key() {
    var libd_lib = Process.findModuleByName("libd-lib.so");
    console.log("libd-lib base address: " + libd_lib.base);
    var des_key_func_off = 0xBC0;
    var des_key_func_addr = libd_lib.base.add(des_key_func_off);
    Interceptor.attach(des_key_func_addr, {
        onEnter: function (args) {
        },
        onLeave: function (ret) {
            console.log("des_key -> leave");
            var des_key_str = ret.readCString();
            console.log("des_key_str: " + des_key_str);
        }
    });
}

function hook_signature() {
    let cihai = Java.use("p.cihai");
    cihai["search"].implementation = function (str) {
        console.log(`cihai.search is called: ${str}`);
        let result = this["search"](str);
        console.log(`cihai.search result=${result}`);
        return result;
    };
    let RunnableC0996b = Java.use("um.b$b");
    RunnableC0996b["run"].implementation = function () {
        console.log(`RunnableC0996b.run is called`);
        this["run"]();
    };
}

function hook_bind_tags() {
    let RestApiClient = Java.use("com.yuewen.push.net.RestApiClient");
    RestApiClient["getBindAliasCall"].implementation = function (str, str2, str3, str4) {
        console.log(`RestApiClient.getBindAliasCall is called: str=${str}, str2=${str2}, str3=${str3}, str4=${str4}`);
        let result = this["getBindAliasCall"](str, str2, str3, str4);
        console.log(`RestApiClient.getBindAliasCall result=${result}`);
        return result;
    };
}

function hook_get_cookie() {
    let c = Java.use("we.c");
    // c["N"].implementation = function (j10, str) {
    //     console.log(`c.N is called: j10=${j10}, str=${str}`);
    //     let result = this["N"](j10, str);
    //     console.log(`c.N result=${result}`);
    //     return result;
    // };
    // c["E"].implementation = function (str, str2) {
    //     console.log(`c.E is called: str=${str}, str2=${str2}`);
    //     let result = this["E"](str, str2);
    //     console.log(`c.E result=${result}`);
    //     return result;
    // };
    // let QDUserManager = Java.use("com.qidian.QDReader.component.user.QDUserManager");
    // QDUserManager["J"].implementation = function (str, str2, str3, str4) {
    //     console.log(`QDUserManager.J is called: str=${str}, str2=${str2}, str3=${str3}, str4=${str4}`);

    //     var stackTrace = Java.use('java.lang.Thread').currentThread().getStackTrace();
    //     // 打印调用栈
    //     console.log('Call stack:');
    //     for (var i = 0; i < stackTrace.length; i++) {
    //         console.log(stackTrace[i].toString());
    //     }

    //     this["J"](str, str2, str3, str4);
    // };

    let QDHttpClient = Java.use("com.qidian.QDReader.framework.network.qd.QDHttpClient");
    QDHttpClient["m"].implementation = function (str, contentValues) {
        console.log(`QDHttpClient.m is called: str=${str}, contentValues=${contentValues}`);
        let result = this["m"](str, contentValues);
        console.log(`QDHttpClient.m result=${result}`);
        return result;
    };

    let QDHttpResp = Java.use("com.qidian.QDReader.framework.network.qd.QDHttpResp");
    QDHttpResp["$init"].overload('boolean', 'int', 'int', 'java.lang.String', 'long').implementation = function (z10, i10, i11, str, j10) {
        if (str.indexOf("Cmfu") >= 0) {
            console.log(`QDHttpResp.$init is called: z10=${z10}, i10=${i10}, i11=${i11}, str=${str}, j10=${j10}`);
            
            var stackTrace = Java.use('java.lang.Thread').currentThread().getStackTrace();
            console.log('Call stack:');
            for (var i = 0; i < stackTrace.length; i++) {
                console.log(stackTrace[i].toString());
            }
        }
        this["$init"](z10, i10, i11, str, j10);
    };

    
}

function hook_sdk_sign() {
    // let Fock = Java.use("com.yuewen.fock.Fock");
    // Fock["sign"].implementation = function (str) {
    //     console.log(`Fock.sign is called: str=${str}`);
    //     let result = this["sign"](str);
    //     console.log(`Fock.sign result=${result}`);
    //     return result;
    // };

    // let c = Java.use("a.c");
    // c["signParams"].implementation = function (context, str, str2, str3, str4, str5, i10, z10) {
    //     console.log(`c.signParams is called: context=${context}, str=${str}, str2=${str2}, str3=${str3}, str4=${str4}, str5=${str5}, i10=${i10}, z10=${z10}`);
        
    //     var stackTrace = Java.use('java.lang.Thread').currentThread().getStackTrace();
    //     console.log('Call stack:');
    //     for (var i = 0; i < stackTrace.length; i++) {
    //         console.log(stackTrace[i].toString());
    //     }
    //     let result = this["signParams"](context, str, str2, str3, str4, str5, i10, z10);
    //     // console.log(`c.signParams result=${result}`);
    //     return result;
    // };

    // let v0 = Java.use("ue.v0");
    // v0["h"].implementation = function (str, str1, str2, str3) {
    //     console.log(`v0.h is called: str=${str}, str=${str1}, str=${str2}, str=${str3}`);
    //     let result = this["h"](str, str1, str2, str3);
    //     console.log(`v0.h result=${result}`);
    //     return result;
    // };

    // let judian = Java.use("ue.judian");
    // judian["search"].implementation = function (jSONObject, i10) {
    //     console.log(`judian.search is called: jSONObject=${jSONObject}, i10=${i10}`);
    //     let result = this["search"](jSONObject, i10);
    //     console.log(`judian.search result=${result}`);
    //     return result;
    // };

    // let Builder = Java.use("okhttp3.Request$Builder");
    // Builder["addHeader"].implementation = function (str, str2) {
    //     if (str.indexOf("SDKSign") >= 0) {
    //         console.log(`Builder.addHeader is called: str=${str}, str2=${str2}`);
    //         var stackTrace = Java.use('java.lang.Thread').currentThread().getStackTrace();
    //         console.log('Call stack:');
    //         for (var i = 0; i < stackTrace.length; i++) {
    //             console.log(stackTrace[i].toString());
    //         }
    //     }
    //     let result = this["addHeader"](str, str2);
    //     // console.log(`Builder.addHeader result=${result}`);
    //     return result;
    // };

    // let l = Java.use("com.qidian.QDReader.framework.webview.l");
    // l["e"].implementation = function (jSONObject, i10) {
    //     console.log(`l.e is called: jSONObject=${jSONObject}, i10=${i10}`);
    //     let result = this["e"](jSONObject, i10);
    //     console.log(`l.e result=${result}`);
    //     return result;
    // };

    // let a = Java.use("b7.a");
    // a["judian"].implementation = function (jSONObject, i10, j10) {
    //     console.log(`a.judian is called: jSONObject=${jSONObject}, i10=${i10}, j10=${j10}`);
    //     let result = this["judian"](jSONObject, i10, j10);
    //     console.log(`a.judian result=${result}`);
    //     return result;
    // };

    // let c = Java.use("a.c");
    // c["signParams"].implementation = function (context, str, str2, str3, str4, str5, i10, z10) {
    //     console.log(`c.signParams is called: context=${context}, str=${str}, str2=${str2}, str3=${str3}, str4=${str4}, str5=${str5}, i10=${i10}, z10=${z10}`);
    //     let result = this["signParams"](context, str, str2, str3, str4, str5, i10, z10);
    //     console.log(`c.signParams result=${result}`);
    //     return result;
    // };

    // let Fock = Java.use("com.yuewen.fock.Fock");
    // Fock["sign"].implementation = function (str) {
    //     console.log(`Fock.sign is called: str=${str}`);
    //     let result = this["sign"](str);
    //     console.log(`Fock.sign result=${result}`);
    //     return result;
    // };

    // var libfock = Process.findModuleByName("libfock.so");
    // console.log("libfock base address: " + libfock.base);
    // var jump_func_off = 0x8E20;
    // var jump_func_addr = libfock.base.add(jump_func_off);
    // Interceptor.attach(jump_func_addr, {
    //     onEnter: function (args) {
    //         console.log(`reg x8 value: ${this.context.x8}`)
    //     },
    //     onLeave: function (ret) {
    //     }
    // });

    // var libc_lib = Process.findModuleByName("libc-lib.so");
    // console.log("libc-lib base address: " + libc_lib.base);
    // var des_func_off = 0x12AC;
    // var des_func_addr = libc_lib.base.add(des_func_off);
    // Interceptor.attach(des_func_addr, {
    //     onEnter: function (args) {
    //         console.log(`des_func is called: ${args[0].readCString()}`);
    //         console.log(`des_func is called: ${args[2]}`);
    //     },
    //     onLeave: function (ret) {
    //     }
    // });

    // var libc_lib = Process.findModuleByName("libc-lib.so");
    // console.log("libc-lib base address: " + libc_lib.base);
    // var des_key_func_off = 0x14C8;
    // var des_key_func_addr = libc_lib.base.add(des_key_func_off);
    // Interceptor.attach(des_key_func_addr, {
    //     onEnter: function (args) {
    //         console.log(`des_key_func is called: ${args[1].readCString()}`);
    //     },
    //     onLeave: function (ret) {
    //     }
    // });

    let a = Java.use("b7.a");
    a["judian"].implementation = function (jSONObject, i10, j10) {
        console.log(`a.judian is called: jSONObject=${jSONObject}, i10=${i10}, j10=${j10}`);
        let result = this["judian"](jSONObject, i10, j10);
        console.log(`a.judian result=${result}`);
        return result;
    };
    // let c = Java.use("a.c");
    // c["signParams"].implementation = function (context, str, str2, str3, str4, str5, i10, z10) {
    //     console.log(`c.signParams is called: context=${context}, str=${str}, str2=${str2}, str3=${str3}, str4=${str4}, str5=${str5}, i10=${i10}, z10=${z10}`);
    //     let result = this["signParams"](context, str, str2, str3, str4, str5, i10, z10);
    //     console.log(`c.signParams result=${result}`);
    //     return result;
    // };

}

Java.perform(function () {
    hook_android_dlopen_ext();
    setTimeout(() => {
        // hook_3des_key();
        // hook_signature();
        // hook_bind_tags();
        // hook_get_cookie();
        hook_sdk_sign();
      }, 1000); 
});
// Java.perform(function () {
//     // var enumMoudle = Process.enumerateModules();
//     // for (var i = 0; i < enumMoudle.length; i++){
//     //     console.log("", enumMoudle[i].name)
//     // }
//     var libmsaoaidsec = Module.getBaseAddress("linker64");
//     console.log("libmsaoaidsec base address: " + libmsaoaidsec);

// });

