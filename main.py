if __name__ == '__main__':

    import sys
    from package import fishtank

    ft_engine = fishtank.FishTankEngine(sys.argv)
    sys.exit(ft_engine.exec())