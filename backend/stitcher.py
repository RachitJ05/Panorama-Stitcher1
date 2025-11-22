import cv2
import numpy as np
import os

def largest_rect_in_hist(heights):
    stack = []
    max_area = 0
    best_l = best_r = best_h = 0
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            H = heights[stack[-1]]
            stack.pop()
            l = stack[-1] + 1 if stack else 0
            r = i - 1
            area = H * (r - l + 1)
            if area > max_area:
                max_area = area
                best_l, best_r, best_h = l, r, H
        stack.append(i)
    return max_area, best_l, best_r, best_h

def geometric_crop_with_visuals(pano):
    h, w = pano.shape[:2]
    gray = cv2.cvtColor(pano, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(gray, 2, 255, cv2.THRESH_BINARY)
    kernel = np.ones((25, 25), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    mask_bin = (mask // 255).astype(int)
    heights = [0] * w
    best_area = 0
    best_rect = (0,0,0,0)

    for row in range(h):
        for col in range(w):
            if mask_bin[row, col] == 1:
                heights[col] += 1
            else:
                heights[col] = 0
        area, l, r, H = largest_rect_in_hist(heights)
        if area > best_area and H > 0:
            best_area = area
            y2 = row
            y1 = row - H + 1
            x1 = l
            x2 = r
            best_rect = (x1, y1, x2, y2)

    x1, y1, x2, y2 = best_rect

    # safe guards
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w-1, x2)
    y2 = min(h-1, y2)

    minRect = np.zeros_like(gray)
    if y2 >= y1 and x2 >= x1:
        minRect[y1:y2+1, x1:x2+1] = 255
    else:
        # fallback: whole image
        minRect[:, :] = 255
        x1, y1, x2, y2 = 0, 0, w-1, h-1

    final_overlay = pano.copy()
    cv2.rectangle(final_overlay, (x1,y1), (x2,y2), (0,0,255), 4)

    contour_overlay = pano.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contour_overlay, contours, -1, (0,255,0), 3)

    cropped = pano[y1:y2+1, x1:x2+1]

    return cropped, minRect, final_overlay, mask, contour_overlay

def stitch_images(image_paths, out_dir='uploads'):
    # read images
    images = [cv2.imread(p) for p in image_paths]
    # optional: resize to a max width to speed up for large inputs
    max_w = 1600
    for i,im in enumerate(images):
        if im is None:
            raise ValueError(f'Failed to load {image_paths[i]}')
        h,w = im.shape[:2]
        if w > max_w:
            scale = max_w / w
            images[i] = cv2.resize(im, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)

    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(images)
    if status != cv2.STITCHER_OK and status != 0:
        raise RuntimeError(f"Stitcher failed with status {status}")

    stitched_name = os.path.join(out_dir, 'stitched.png')
    cv2.imwrite(stitched_name, stitched)

    # run geometric crop
    cropped, minRect, overlay, mask, contour_overlay = geometric_crop_with_visuals(stitched)

    cropped_name = os.path.join(out_dir, 'stitched_cropped.png')
    overlay_name = os.path.join(out_dir, 'overlay.png')
    contour_name = os.path.join(out_dir, 'contour.png')
    mask_name = os.path.join(out_dir, 'mask.png')

    cv2.imwrite(cropped_name, cropped)
    cv2.imwrite(overlay_name, overlay)
    cv2.imwrite(contour_name, contour_overlay)
    cv2.imwrite(mask_name, mask)

    return {
        'stitched': stitched_name,
        'cropped': cropped_name,
        'overlay': overlay_name,
        'contour': contour_name,
        'mask': mask_name
    }
