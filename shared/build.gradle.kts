plugins {
    id("com.android.library")
    id("org.jetbrains.kotlin.multiplatform")
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions.jvmTarget = "17"
        }
    }

    val isMacHost = System.getProperty("os.name").startsWith("Mac OS X", ignoreCase = true)
    if (isMacHost) {
        iosX64()
        iosArm64()
        iosSimulatorArm64()
    }

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.1")
            }
        }
        val commonTest by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
                implementation(kotlin("test"))
            }
        }
        val androidMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
                implementation("androidx.room:room-runtime:2.6.1")
                implementation("androidx.room:room-ktx:2.6.1")
            }
        }
        val androidUnitTest by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
                implementation(kotlin("test"))
            }
        }
    }
}

android {
    namespace = "com.soilandsupper.shared"
    compileSdk = 34
    defaultConfig {
        minSdk = 24
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
