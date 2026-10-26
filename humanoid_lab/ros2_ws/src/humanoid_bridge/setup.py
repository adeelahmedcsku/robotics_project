from setuptools import setup
setup(name='humanoid_bridge', version='0.1.0',
      packages=['humanoid_bridge'],
      data_files=[('share/ament_index/resource_index/packages', ['resource/humanoid_bridge']),
                  ('share/humanoid_bridge', ['package.xml']),
                  ('share/humanoid_bridge/launch', ['launch/lab.launch.py'])],
      install_requires=['setuptools'], zip_safe=True,
      maintainer='Robotics Lab', maintainer_email='student@example.org',
      description='Simulation teaching bridge', license='MIT',
      entry_points={'console_scripts': [
          'bridge = humanoid_bridge.bridge:main',
          'wave = humanoid_bridge.wave:main']})
