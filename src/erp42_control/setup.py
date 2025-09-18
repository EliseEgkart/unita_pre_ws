from setuptools import find_packages, setup

package_name = 'erp42_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='songsong',
    maintainer_email='whwoals159874@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'erp_status_node = erp42_control.erp_status:main',
            'ByteHandler_node = erp42_control.ByteHandler:main',
            'ErpSerialHandler_node = erp42_control.ErpSerialHandler:main',
        ],
    },
)
