#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreMedia/CoreMedia.h>
#import <ImageIO/ImageIO.h>
#import <CoreGraphics/CoreGraphics.h>

/**
 * Native macOS AVFoundation LivePhoto Synthesizer
 * Merges target video stream with authentic host/capsule mebx metadata tracks,
 * sets QuickTime ContentIdentifier UUID, and extracts first frame (t=0) as reference JPG.
 */
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc < 5) {
            fprintf(stderr, "Usage: %s <target_video> <capsule_mov> <output_mov> <output_jpg> [uuid]\n", argv[0]);
            return 1;
        }

        NSString *targetVideoPath = [NSString stringWithUTF8String:argv[1]];
        NSString *capsuleVideoPath = [NSString stringWithUTF8String:argv[2]];
        NSString *outputVideoPath = [NSString stringWithUTF8String:argv[3]];
        NSString *outputImagePath = [NSString stringWithUTF8String:argv[4]];
        NSString *assetIdentifier = (argc >= 6) ? [NSString stringWithUTF8String:argv[5]] : [[NSUUID UUID] UUIDString];

        NSFileManager *fm = [NSFileManager defaultManager];
        [fm removeItemAtPath:outputVideoPath error:nil];
        [fm removeItemAtPath:outputImagePath error:nil];

        AVURLAsset *targetAsset = [AVURLAsset assetWithURL:[NSURL fileURLWithPath:targetVideoPath]];
        AVURLAsset *capsuleAsset = [AVURLAsset assetWithURL:[NSURL fileURLWithPath:capsuleVideoPath]];

        AVMutableComposition *composition = [AVMutableComposition composition];

        // 1. Video track from target asset
        NSArray<AVAssetTrack *> *targetVideoTracks = [targetAsset tracksWithMediaType:AVMediaTypeVideo];
        if (targetVideoTracks.count == 0) {
            fprintf(stderr, "Error: No video track found in target video: %s\n", targetVideoPath.UTF8String);
            return 1;
        }
        AVAssetTrack *targetVideoTrack = targetVideoTracks[0];
        AVMutableCompositionTrack *compVideoTrack = [composition addMutableTrackWithMediaType:AVMediaTypeVideo preferredTrackID:kCMPersistentTrackID_Invalid];

        CMTime targetDuration = targetAsset.duration;
        NSError *err = nil;
        [compVideoTrack insertTimeRange:CMTimeRangeMake(kCMTimeZero, targetDuration) ofTrack:targetVideoTrack atTime:kCMTimeZero error:&err];
        if (err) {
            fprintf(stderr, "Error inserting target video track: %s\n", err.localizedDescription.UTF8String);
            return 1;
        }
        compVideoTrack.preferredTransform = targetVideoTrack.preferredTransform;

        // 2. Audio track (if present in target)
        NSArray<AVAssetTrack *> *targetAudioTracks = [targetAsset tracksWithMediaType:AVMediaTypeAudio];
        if (targetAudioTracks.count > 0) {
            AVAssetTrack *targetAudioTrack = targetAudioTracks[0];
            AVMutableCompositionTrack *compAudioTrack = [composition addMutableTrackWithMediaType:AVMediaTypeAudio preferredTrackID:kCMPersistentTrackID_Invalid];
            [compAudioTrack insertTimeRange:CMTimeRangeMake(kCMTimeZero, CMTimeMinimum(targetAudioTrack.timeRange.duration, targetDuration)) ofTrack:targetAudioTrack atTime:kCMTimeZero error:nil];
        }

        // 3. Metadata tracks (mebx motion tracks) from capsule
        NSArray<AVAssetTrack *> *capsuleMetaTracks = [capsuleAsset tracksWithMediaType:AVMediaTypeMetadata];
        for (AVAssetTrack *metaTrack in capsuleMetaTracks) {
            AVMutableCompositionTrack *compMetaTrack = [composition addMutableTrackWithMediaType:AVMediaTypeMetadata preferredTrackID:kCMPersistentTrackID_Invalid];
            [compMetaTrack insertTimeRange:metaTrack.timeRange ofTrack:metaTrack atTime:kCMTimeZero error:&err];
            [compMetaTrack addTrackAssociationToTrack:compVideoTrack type:AVTrackAssociationTypeMetadataReferent];
        }

        // 4. QuickTime Container Metadata items
        NSMutableArray<AVMetadataItem *> *metaItems = [NSMutableArray array];
        for (AVMetadataItem *item in capsuleAsset.metadata) {
            if ([item.key isEqual:@"com.apple.quicktime.content.identifier"] ||
                [item.key isEqual:@"com.apple.quicktime.still-image-time"]) {
                continue;
            }
            [metaItems addObject:[item mutableCopy]];
        }

        // Content Identifier (UUID)
        AVMutableMetadataItem *cidItem = [AVMutableMetadataItem new];
        cidItem.key = @"com.apple.quicktime.content.identifier";
        cidItem.keySpace = AVMetadataKeySpaceQuickTimeMetadata;
        cidItem.value = assetIdentifier;
        [metaItems addObject:cidItem];

        // Still image time (0)
        AVMutableMetadataItem *sitItem = [AVMutableMetadataItem new];
        sitItem.key = @"com.apple.quicktime.still-image-time";
        sitItem.keySpace = AVMetadataKeySpaceQuickTimeMetadata;
        sitItem.value = @(0);
        [metaItems addObject:sitItem];

        // 5. Export passthrough
        AVAssetExportSession *exporter = [[AVAssetExportSession alloc] initWithAsset:composition presetName:AVAssetExportPresetPassthrough];
        exporter.outputURL = [NSURL fileURLWithPath:outputVideoPath];
        exporter.outputFileType = AVFileTypeQuickTimeMovie;
        exporter.metadata = metaItems;

        dispatch_semaphore_t sema = dispatch_semaphore_create(0);
        __block BOOL exportOk = NO;
        [exporter exportAsynchronouslyWithCompletionHandler:^{
            if (exporter.status == AVAssetExportSessionStatusCompleted) {
                exportOk = YES;
            } else {
                fprintf(stderr, "Export error: %s\n", exporter.error.localizedDescription.UTF8String);
            }
            dispatch_semaphore_signal(sema);
        }];
        dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER);

        if (!exportOk) {
            return 1;
        }

        // 6. Extract initial frame at t=0
        AVAssetImageGenerator *gen = [AVAssetImageGenerator assetImageGeneratorWithAsset:targetAsset];
        gen.appliesPreferredTrackTransform = YES;
        gen.requestedTimeToleranceBefore = kCMTimeZero;
        gen.requestedTimeToleranceAfter = kCMTimeZero;

        CGImageRef imgRef = [gen copyCGImageAtTime:kCMTimeZero actualTime:nil error:&err];
        if (!imgRef) {
            fprintf(stderr, "Image extraction failed: %s\n", err.localizedDescription.UTF8String);
            return 1;
        }

        NSURL *outImgURL = [NSURL fileURLWithPath:outputImagePath];
        CGImageDestinationRef dest = CGImageDestinationCreateWithURL((__bridge CFURLRef)outImgURL, (CFStringRef)@"public.jpeg", 1, NULL);
        CGImageDestinationAddImage(dest, imgRef, NULL);
        CGImageDestinationFinalize(dest);
        CFRelease(dest);
        CGImageRelease(imgRef);

        return 0;
    }
}
