package com.soilandsupper.ui

import android.graphics.BitmapFactory
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.unit.dp
import com.soilandsupper.domain.model.MockPlantIdentifier
import com.soilandsupper.shared.domain.model.PlantIdentification
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch

@Composable
fun IdentifyScreen(plantIdentifier: MockPlantIdentifier) {
    val context = androidx.compose.ui.platform.LocalContext.current
    var selectedBitmap by remember { mutableStateOf<android.graphics.Bitmap?>(null) }
    var identification by remember { mutableStateOf<PlantIdentification?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }

    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri ->
            uri?.let {
                selectedBitmap = BitmapFactory.decodeStream(
                    context.contentResolver.openInputStream(it)
                )
            }
        }
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Button(
            onClick = {
                photoPickerLauncher.launch(
                    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                )
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Select Photo")
        }

        selectedBitmap?.let { bitmap ->
            Image(
                bitmap = bitmap.asImageBitmap(),
                contentDescription = "Selected plant",
                modifier = Modifier.fillMaxWidth()
            )
            Button(
                onClick = {
                    isLoading = true
                    error = null
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading
            ) {
                Text(if (isLoading) "Identifying..." else "Identify")
            }
        }

        identification?.let { result ->
            Text(text = "Plant: ${result.cropName}")
            if (result.variety.isNotBlank()) {
                Text(text = "Variety: ${result.variety}")
            }
            Text(text = "Confidence: ${(result.confidence * 100).toInt()}%")
        }

        error?.let {
            Text(text = "Error: $it", color = androidx.compose.material3.MaterialTheme.colorScheme.error)
        }
    }

    LaunchedEffect(selectedBitmap, isLoading) {
        if (isLoading && selectedBitmap != null) {
            try {
                val result = plantIdentifier.identify(selectedBitmap!!)
                identification = result
            } catch (e: Exception) {
                error = e.message
            } finally {
                isLoading = false
            }
        }
    }
}
