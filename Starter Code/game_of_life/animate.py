import imageio
import numpy
import pygame


def animate_surfaces(surfaces: list[pygame.Surface], video_path: str) -> None:
    """
    Writes a list of pygame.Surface objects to an MP4 video, one surface per frame.

    Parameters:
    - surfaces: list of pygame.Surface objects (the frames)
    - video_path: file path of the MP4 video to write

    Output:
    - None: the video is written to video_path.
    """
    writer = imageio.get_writer(video_path, fps=10, codec="libx264", quality=8)

    for surface in surfaces:
        writer.append_data(surface_to_numpy(surface))

    writer.close()


def surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """
    Converts a pygame.Surface to a NumPy RGB array of shape (height, width, 3).
    pygame indexes pixels as (x, y), but images are indexed (row, col), so we swap axes.

    Parameters:
    - surface: the pygame.Surface to convert

    Output:
    - numpy.ndarray with one RGB triple per pixel.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)
